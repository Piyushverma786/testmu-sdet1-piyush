"""
AI Test Case Generator Script
==============================
Run this script to use LLM to generate test case ideas.
Output is saved to AI_GENERATED_TEST_IDEAS.md

Usage: python utils/generate_test_cases.py
"""

from llm_helper import generate_test_cases
import json
from datetime import datetime


def main():
    modules = [
        {
            "name": "Login Module",
            "description": "A login page with username and password fields, submit button, "
                           "and error messages. Supports session management and redirects on success."
        },
        {
            "name": "Dashboard Module",
            "description": "A task management dashboard where users can create, edit, complete, "
                           "and delete tasks. Supports filtering by status (all/active/completed)."
        },
        {
            "name": "REST API Module",
            "description": "A REST API supporting CRUD operations on posts, users, comments, and todos. "
                           "Returns JSON responses with standard HTTP status codes."
        }
    ]
    
    output = [
        f"# AI-Generated Test Cases",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Generated using: GPT-4o-mini via OpenAI API",
        f"Prompt strategy: Module description → structured JSON output\n",
        "---\n"
    ]
    
    for module in modules:
        print(f"Generating test cases for: {module['name']}...")
        test_cases = generate_test_cases(module["name"], module["description"])
        
        output.append(f"## {module['name']}")
        output.append(f"**Module Description:** {module['description']}\n")
        
        if test_cases:
            for tc in test_cases:
                output.append(f"### {tc.get('test_id', 'TC')} - {tc.get('title', 'Untitled')}")
                output.append(f"**Category:** {tc.get('category', 'N/A')}")
                output.append(f"**Steps:**")
                for step in tc.get('steps', []):
                    output.append(f"  - {step}")
                output.append(f"**Expected Result:** {tc.get('expected_result', 'N/A')}\n")
        else:
            output.append("*Could not generate test cases (LLM unavailable)*\n")
        
        output.append("---\n")
    
    with open("AI_GENERATED_TEST_IDEAS.md", "w") as f:
        f.write("\n".join(output))
    
    print("\n✅ Test cases saved to AI_GENERATED_TEST_IDEAS.md")


if __name__ == "__main__":
    main()
