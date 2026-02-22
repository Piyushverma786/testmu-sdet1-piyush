"""
Login Module Tests
==================
Test cases generated with AI assistance (GPT-4o-mini via LLM helper).
Prompt used: "Generate comprehensive Playwright test cases for a login page
with username/password fields, covering positive, negative, edge, and security scenarios."

Target: https://practicetestautomation.com/practice-test-login/
(Public demo site - safe for hackathon use)
"""

import pytest
from playwright.sync_api import Page, expect


BASE = "https://practicetestautomation.com/practice-test-login/"
VALID_USER = "student"
VALID_PASS = "Password123"


@pytest.mark.login
@pytest.mark.smoke
class TestLoginPositive:
    """AI-Generated Category: Positive / Happy Path Tests"""

    def test_TC001_valid_login_success(self, page: Page):
        """TC001: Valid credentials should log user in successfully."""
        page.goto(BASE)
        page.fill("#username", VALID_USER)
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        # Assert successful login
        expect(page).to_have_url(
            "https://practicetestautomation.com/logged-in-successfully/"
        )
        expect(page.locator("h1")).to_contain_text("Logged In Successfully")

    def test_TC002_login_page_loads_correctly(self, page: Page):
        """TC002: Login page should display all required elements."""
        page.goto(BASE)
        
        expect(page.locator("#username")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        expect(page.locator("#submit")).to_be_visible()
        expect(page.locator("#submit")).to_be_enabled()

    def test_TC003_page_title_is_correct(self, page: Page):
        """TC003: Login page title should be correct."""
        page.goto(BASE)
        # Site title may vary; accept known variants
        title = page.title()
        assert "Test Login" in title and "Practice" in title

    def test_TC004_logout_after_login(self, page: Page):
        """TC004: User should be able to log out after login."""
        page.goto(BASE)
        page.fill("#username", VALID_USER)
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        # Find and click logout
        logout_btn = page.locator("text=Log out")
        expect(logout_btn).to_be_visible()
        logout_btn.click()
        
        # Should return to login page
        expect(page).to_have_url(BASE)


@pytest.mark.login
@pytest.mark.regression
class TestLoginNegative:
    """AI-Generated Category: Negative / Error Handling Tests"""

    def test_TC005_invalid_username(self, page: Page):
        """TC005: Invalid username should show error message."""
        page.goto(BASE)
        page.fill("#username", "wronguser")
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        error = page.locator("#error")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Your username is invalid!")

    def test_TC006_invalid_password(self, page: Page):
        """TC006: Invalid password should show error message."""
        page.goto(BASE)
        page.fill("#username", VALID_USER)
        page.fill("#password", "wrongpassword")
        page.click("#submit")
        
        error = page.locator("#error")
        expect(error).to_be_visible()
        expect(error).to_contain_text("Your password is invalid!")

    def test_TC007_empty_username(self, page: Page):
        """TC007: Empty username should show validation error."""
        page.goto(BASE)
        page.fill("#username", "")
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        error = page.locator("#error")
        expect(error).to_be_visible()

    def test_TC008_empty_password(self, page: Page):
        """TC008: Empty password should show validation error."""
        page.goto(BASE)
        page.fill("#username", VALID_USER)
        page.fill("#password", "")
        page.click("#submit")
        
        error = page.locator("#error")
        expect(error).to_be_visible()

    def test_TC009_both_fields_empty(self, page: Page):
        """TC009: Both fields empty should show error."""
        page.goto(BASE)
        page.click("#submit")
        
        error = page.locator("#error")
        expect(error).to_be_visible()

    def test_TC010_case_sensitive_username(self, page: Page):
        """TC010: Username should be case-sensitive."""
        page.goto(BASE)
        page.fill("#username", "STUDENT")  # uppercase - should fail
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        error = page.locator("#error")
        expect(error).to_be_visible()


@pytest.mark.login
@pytest.mark.regression
class TestLoginEdgeCases:
    """AI-Generated Category: Edge Cases & Security"""

    def test_TC011_whitespace_in_username(self, page: Page):
        """TC011: Username with leading/trailing spaces."""
        page.goto(BASE)
        page.fill("#username", "  student  ")
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        # Should fail — whitespace is not trimmed or it's invalid
        error = page.locator("#error")
        expect(error).to_be_visible()

    def test_TC012_special_chars_in_fields(self, page: Page):
        """TC012: Special characters in username field."""
        page.goto(BASE)
        page.fill("#username", "<script>alert('xss')</script>")
        page.fill("#password", "test")
        page.click("#submit")
        
        # Page should not execute script — error shown
        error = page.locator("#error")
        expect(error).to_be_visible()
        
        # Verify XSS didn't execute
        assert "alert" not in page.title()

    def test_TC013_password_field_masked(self, page: Page):
        """TC013: Password field input should be masked (type=password)."""
        page.goto(BASE)
        password_field = page.locator("#password")
        field_type = password_field.get_attribute("type")
        assert field_type == "password", f"Expected 'password' type, got '{field_type}'"

    def test_TC014_sql_injection_attempt(self, page: Page):
        """TC014: SQL injection in username should be handled safely."""
        page.goto(BASE)
        page.fill("#username", "' OR '1'='1")
        page.fill("#password", "' OR '1'='1")
        page.click("#submit")
        
        # Should show error, not log in
        error = page.locator("#error")
        expect(error).to_be_visible()

    def test_TC015_very_long_username(self, page: Page):
        """TC015: Very long username should not crash the page."""
        page.goto(BASE)
        long_username = "a" * 1000
        page.fill("#username", long_username)
        page.fill("#password", VALID_PASS)
        page.click("#submit")
        
        # Page should remain stable
        expect(page.locator("#submit")).to_be_visible()
