# AI Usage Log

> This document tracks every AI tool used during this hackathon assignment,
> what it was used for, the exact prompt strategy, and the outcome.
> Transparency in AI usage is a core requirement of this submission.

---

## Summary

| # | Tool | Purpose | Outcome |
|---|------|---------|---------|
| 1 | GPT-4o-mini (OpenAI API) | Generate login test cases | 15 test cases generated, 10 implemented |
| 2 | GPT-4o-mini (OpenAI API) | Generate dashboard test cases | 12 test cases generated, 11 implemented |
| 3 | GPT-4o-mini (OpenAI API) | Generate API test cases | 14 test cases generated, all implemented |
| 4 | GPT-4o-mini (OpenAI API) | Failure Explainer (runtime) | Wired into conftest.py pytest hook |
| 5 | GPT-4o-mini (OpenAI API) | Flaky Test Classifier (runtime) | Classifies failures on every test run |
| 6 | Claude (Anthropic) | Project architecture review | Suggested conftest hook pattern |

---

## Detailed Usage

### 1. Login Test Case Generation

**Tool:** OpenAI GPT-4o-mini via API (`utils/llm_helper.py → generate_test_cases()`)  
**When:** Pre-implementation planning phase  
**Prompt Strategy:**
```
You are a senior QA engineer. Generate comprehensive test cases for:
Module: Login Module
Description: A login page with username and password fields, submit button,
and error messages. Supports session management and redirects on success.

Generate 8-10 test cases covering: happy path, edge cases, negative tests, security basics.
Respond ONLY with valid JSON array: [{"test_id": ..., "title": ..., "category": ..., "steps": [...], "expected_result": ...}]
```

**Output:** 10 test cases covering positive, negative, edge, and security categories  
**How AI output was used:** Used the AI's test case ideas as the blueprint, then manually implemented each in Playwright with real locators and assertions  
**Manual work added:** Correct CSS selectors, Playwright-specific API calls, proper assertions  

---

### 2. Dashboard Test Case Generation

**Tool:** OpenAI GPT-4o-mini  
**When:** Pre-implementation  
**Prompt Strategy:** Same structured prompt, module = "Dashboard Module" with TodoMVC description  
**Output:** 12 test cases covering CRUD, filters, and edge cases  
**How used:** Mapped AI suggestions to Playwright test methods; some AI-suggested cases were merged (e.g., "create task" + "verify count" became one test)  

---

### 3. REST API Test Case Generation

**Tool:** OpenAI GPT-4o-mini  
**When:** Pre-implementation  
**Prompt Strategy:** Same pattern, API module with CRUD, status codes, schema validation emphasis  
**Output:** 14 test cases  
**How used:** Implemented directly using Python `requests` library; AI correctly suggested schema validation pattern  

---

### 4. AI Failure Explainer (Runtime Feature)

**Tool:** OpenAI GPT-4o-mini  
**When:** Runtime — called automatically when any test fails  
**Location:** `conftest.py → pytest_runtest_makereport hook` + `utils/llm_helper.py → explain_failure()`  
**Prompt Strategy:**
```
You are an expert QA engineer. A Playwright test has failed.
Test Name: {test_name}
Error Message: {error_message}
Stack Trace: {stack_trace}

Please provide:
1. A plain-English explanation of what went wrong (2-3 sentences)
2. The most likely root cause
3. A specific fix suggestion

Format as:
EXPLANATION: ...
ROOT CAUSE: ...
FIX: ...
```
**Outcome:** When a test fails, QA sees an actionable AI explanation instantly in the console  
**Value added:** Reduces time-to-fix by giving developers plain-English context without reading raw Playwright errors  

---

### 5. Flaky Test Classifier (Runtime Feature)

**Tool:** OpenAI GPT-4o-mini  
**When:** Runtime — called alongside Failure Explainer on every failure  
**Location:** `conftest.py` + `utils/llm_helper.py → classify_flaky_test()`  
**Prompt Strategy:**
```
Classify this test failure:
- FLAKY: Intermittent failure likely due to timing, network, or environment
- REAL_BUG: Consistent failure indicating actual application defect
- NEEDS_INVESTIGATION: Unclear, requires more data

Respond ONLY with valid JSON: {"classification": ..., "confidence": 0-100, "reason": "..."}
```
**Outcome:** Each failure is tagged FLAKY / REAL_BUG / NEEDS_INVESTIGATION with a confidence score  
**Value added:** Helps triage — a "FLAKY, 90% confidence" failure is deprioritized vs "REAL_BUG, 95% confidence"  

---

### 6. Architecture Consultation

**Tool:** Claude (Anthropic)  
**When:** Design phase  
**How used:** Asked about best way to inject AI into pytest lifecycle. Got recommendation to use `pytest_runtest_makereport` hookwrapper pattern instead of a fixture, which gives access to the full failure report including longrepr  
**Outcome:** Cleaner implementation — AI hook fires reliably on every failure  

---

## What AI Did NOT Do

- AI did not write the final Playwright test code (selectors, assertions, page interactions)
- AI did not choose the test framework (Playwright was chosen by the engineer)
- AI did not select the demo applications used for testing
- AI output was always reviewed and validated before use
- No AI-generated code was copy-pasted blindly

## Reflection

The most valuable AI use was the **runtime Failure Explainer**. Instead of reading a 50-line Playwright stack trace, a failing test now prints:

```
EXPLANATION: The test failed because the expected element '#error' was not found 
within the default timeout, suggesting the login form submitted successfully or 
the error message has a different selector.
ROOT CAUSE: CSS selector mismatch or timing issue with error message rendering.
FIX: Add an explicit wait before asserting the error element, and verify the 
selector matches the current DOM using browser DevTools.
```

This is the kind of AI integration that saves real time in real QA workflows.
