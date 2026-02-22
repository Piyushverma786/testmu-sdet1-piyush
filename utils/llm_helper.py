"""
LLM Helper - Core AI utility for:
1. Failure Explainer: Explains test failures in plain English
2. Flaky Test Classifier: Classifies if a failure is flaky or real
3. Test Case Generator: Generates test ideas using LLM
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-placeholder"))


def explain_failure(test_name: str, error_message: str, stack_trace: str = "") -> str:
    """
    Takes a test failure and returns a plain-English explanation + fix suggestion.
    This is called automatically when any test fails (via conftest.py hook).
    """
    prompt = f"""You are an expert QA engineer. A Playwright test has failed.

Test Name: {test_name}
Error Message: {error_message}
Stack Trace: {stack_trace[:1000] if stack_trace else 'Not available'}

Please provide:
1. A plain-English explanation of what went wrong (2-3 sentences)
2. The most likely root cause
3. A specific fix suggestion

Keep your response concise and actionable. Format as:
EXPLANATION: ...
ROOT CAUSE: ...
FIX: ...
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LLM Unavailable] Could not explain failure: {str(e)}"


def classify_flaky_test(test_name: str, error_message: str, run_history: list = None) -> dict:
    """
    Classifies whether a test failure is likely flaky or a real bug.
    
    Args:
        test_name: Name of the test
        error_message: The error that occurred
        run_history: List of past results e.g. ['pass', 'fail', 'pass', 'fail']
    
    Returns:
        dict with 'classification', 'confidence', 'reason'
    """
    history_str = ", ".join(run_history) if run_history else "No history available"
    
    prompt = f"""You are a QA expert specializing in test reliability.

Test Name: {test_name}
Error Message: {error_message}
Recent Run History: {history_str}

Classify this test failure:
- FLAKY: Intermittent failure likely due to timing, network, or environment
- REAL_BUG: Consistent failure indicating actual application defect
- NEEDS_INVESTIGATION: Unclear, requires more data

Respond ONLY with valid JSON:
{{
  "classification": "FLAKY" | "REAL_BUG" | "NEEDS_INVESTIGATION",
  "confidence": 0-100,
  "reason": "one sentence explanation"
}}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.1
        )
        content = response.choices[0].message.content.strip()
        # Parse JSON safely
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {
            "classification": "NEEDS_INVESTIGATION",
            "confidence": 0,
            "reason": f"LLM unavailable: {str(e)}"
        }


def generate_test_cases(module: str, description: str) -> list:
    """
    Uses LLM to generate test case ideas for a given module.
    Used during test planning — output is logged in AI_USAGE_LOG.md
    """
    prompt = f"""You are a senior QA engineer. Generate comprehensive test cases for:

Module: {module}
Description: {description}

Generate 8-10 test cases covering: happy path, edge cases, negative tests, security basics.

Respond ONLY with valid JSON array:
[
  {{
    "test_id": "TC001",
    "title": "...",
    "category": "positive|negative|edge|security",
    "steps": ["step1", "step2"],
    "expected_result": "..."
  }}
]"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.4
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"[LLM] Could not generate test cases: {e}")
        return []
