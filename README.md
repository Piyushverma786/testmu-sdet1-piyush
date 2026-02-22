# TestMu AI - SDET Hackathon Submission

> **Assignment:** Set up a test framework, use LLMs to generate test cases, wire an LLM into the test pipeline as a Failure Explainer & Flaky Test Classifier.
> <img width="1901" height="892" alt="image" src="https://github.com/user-attachments/assets/daceb86a-5900-4206-95b0-9217b460596c" />

---

## Architecture Overview

```
testmu-ai-sdet/
├── tests/
│   ├── login/
│   │   └── test_login.py          # 15 test cases (TC001–TC015)
│   ├── dashboard/
│   │   └── test_dashboard.py      # 15 test cases (TC101–TC115)
│   └── api/
│       └── test_api.py            # 20 test cases (TC201–TC220)
├── utils/
│   ├── llm_helper.py              # 🤖 Core AI utility (Failure Explainer + Classifier)
│   └── generate_test_cases.py     # Script to generate test ideas via LLM
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
├── conftest.py                    # Pytest config + AI failure hook
├── pytest.ini                     # Test runner config
├── requirements.txt
├── AI_USAGE_LOG.md                # ✅ Full transparency on every AI tool used
└── README.md
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Test Framework | **Playwright** (Python) |
| Test Runner | **pytest** |
| AI Integration | **OpenAI GPT-4o-mini** |
| Reporting | **pytest-html** |
| CI/CD | **GitHub Actions** |
| Language | **Python 3.11** |

---

## Setup & Run

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/testmu-ai-sdet.git
cd testmu-ai-sdet
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run by module
pytest tests/login/ -v
pytest tests/dashboard/ -v
pytest tests/api/ -v

# Run by tag
pytest -m smoke          # Fast smoke tests
pytest -m regression     # Full regression suite
pytest -m "login and regression"

# Generate HTML report
pytest --html=reports/report.html --self-contained-html
```

### 4. Generate AI Test Case Ideas
```bash
cd utils
python generate_test_cases.py
# Output saved to AI_GENERATED_TEST_IDEAS.md
```

---

## AI Features

### 🤖 Feature 1: AI Failure Explainer

When any test fails, the LLM **automatically** explains the failure in plain English:

```
============================================================
🤖 AI FAILURE EXPLAINER - test_TC005_invalid_username
============================================================
EXPLANATION: The test failed because the '#error' element was not visible
within the timeout. The login form may have submitted to a different URL
or the error element's CSS selector has changed.

ROOT CAUSE: Selector mismatch — the error element ID may have been renamed
in a recent UI update.

FIX: Inspect the current DOM with DevTools and update the selector from
'#error' to the correct class or ID. Add page.wait_for_selector() before
the expect() assertion.
============================================================
```

**Implementation:** `conftest.py → pytest_runtest_makereport` hook + `utils/llm_helper.py`

---

### 🏷️ Feature 2: Flaky Test Classifier

Every failure is automatically classified:

```
🏷️  FLAKY CLASSIFIER:
   Classification : FLAKY
   Confidence     : 85%
   Reason         : Timeout errors on dynamic content suggest timing issue
```

Classifications:
- `FLAKY` — Intermittent, likely timing/network/environment issue
- `REAL_BUG` — Consistent failure indicating actual application defect  
- `NEEDS_INVESTIGATION` — Insufficient data to classify

**Value:** Triage instantly — skip retrying `REAL_BUG` failures and add waits to `FLAKY` ones.

---

### 📋 Feature 3: AI-Generated Test Cases

Test cases were generated using LLM prompts before implementation:

```python
generate_test_cases(
    module="Login Module",
    description="A login page with username/password, submit button, error messages..."
)
# Returns structured JSON with test_id, title, category, steps, expected_result
```

The AI output was used as a **blueprint** — all final Playwright code was written manually using the AI's test ideas.

---

## Test Coverage

| Module | Tests | Positive | Negative | Edge/Security |
|--------|-------|----------|----------|---------------|
| Login | 15 | 4 | 6 | 5 |
| Dashboard | 15 | 4 | 6 | 5 |
| REST API | 20 | 8 | 6 | 6 |
| **Total** | **50** | **16** | **18** | **16** |

---

## AI Usage Transparency

See **[AI_USAGE_LOG.md](./AI_USAGE_LOG.md)** for full documentation of:
- Every AI tool used (tool name, model, when, why)
- Exact prompt strategies
- How AI output was used vs. what was done manually
- Reflection on what added the most value

---

## CI/CD

GitHub Actions runs all tests on every push/PR. Configure `OPENAI_API_KEY` in repository secrets.

See `.github/workflows/ci.yml` for the pipeline definition.
