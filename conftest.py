"""
conftest.py - Pytest configuration and fixtures.

Key feature: AI Failure Explainer hook
When any test fails, the LLM automatically explains the failure
and optionally classifies it as flaky or real bug.
"""

import pytest
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.llm_helper import explain_failure, classify_flaky_test

load_dotenv()

# Store failure details for the AI hook
_failure_store = {}


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "login: Login module tests")
    config.addinivalue_line("markers", "dashboard: Dashboard module tests")
    config.addinivalue_line("markers", "api: API module tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://demo.playwright.dev/todomvc")


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def test_credentials():
    return {
        "username": os.getenv("TEST_USERNAME", "admin@testmu.ai"),
        "password": os.getenv("TEST_PASSWORD", "Test@1234")
    }


@pytest.fixture(autouse=True)
def track_test(request):
    """Auto-fixture: tracks test name for failure hook."""
    yield
    # Nothing here — failure hook below handles AI explanation


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    AI FAILURE EXPLAINER HOOK
    
    Runs after each test phase (setup/call/teardown).
    If a test fails during 'call' phase, sends failure to LLM for explanation.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        test_name = item.name
        error_msg = str(report.longrepr) if report.longrepr else "Unknown error"
        
        # Truncate for readability
        error_short = error_msg[:500]
        
        print(f"\n{'='*60}")
        print(f"[AI] FAILURE EXPLAINER - {test_name}")
        print(f"{'='*60}")
        
        # Get AI explanation
        explanation = explain_failure(
            test_name=test_name,
            error_message=error_short,
            stack_trace=error_msg[500:1000]
        )
        # Safe print for Windows cp1252
        try:
            print(explanation)
        except UnicodeEncodeError:
            print(explanation.encode("ascii", "replace").decode("ascii"))
        
        # Classify if flaky
        classification = classify_flaky_test(
            test_name=test_name,
            error_message=error_short
        )
        print(f"\n[FLAKY CLASSIFIER]:")
        print(f"   Classification : {classification.get('classification', 'N/A')}")
        print(f"   Confidence     : {classification.get('confidence', 0)}%")
        print(f"   Reason         : {classification.get('reason', 'N/A')}")
        print(f"{'='*60}\n")
        
        # Attach to report for HTML output
        report.ai_explanation = explanation
        report.ai_classification = classification


def pytest_html_report_title(report):
    report.title = "TestMu AI - SDET Hackathon Test Report"


@pytest.fixture
def browser_context_args(browser_context_args):
    """Extended browser context with common settings."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "reports/videos/" if os.getenv("RECORD_VIDEO") else None,
    }
