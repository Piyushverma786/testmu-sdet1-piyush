"""
Dashboard Module Tests
======================
Test cases AI-generated using GPT-4o-mini.
Prompt: "Generate Playwright test cases for a todo/dashboard web app,
covering page load, CRUD operations, filtering, and UI validations."

Target: https://demo.playwright.dev/todomvc (Playwright's official demo app)
This is a standard TodoMVC app used as a dashboard/task management demo.
"""

import pytest
from playwright.sync_api import Page, expect


BASE = "https://demo.playwright.dev/todomvc"


@pytest.fixture(autouse=True)
def navigate_to_app(page: Page):
    """Navigate to app before each test."""
    page.goto(BASE)
    yield


@pytest.mark.dashboard
@pytest.mark.smoke
class TestDashboardLoad:
    """AI-Generated Category: Page Load & UI Validation"""

    def test_TC101_dashboard_loads_successfully(self, page: Page):
        """TC101: Dashboard/app should load without errors."""
        expect(page.locator(".todoapp")).to_be_visible()

    def test_TC102_page_title_correct(self, page: Page):
        """TC102: Page title should be set correctly."""
        expect(page).to_have_title("React • TodoMVC")

    def test_TC103_input_field_visible_and_enabled(self, page: Page):
        """TC103: Main input field should be visible and ready for input."""
        input_field = page.locator(".new-todo")
        expect(input_field).to_be_visible()
        expect(input_field).to_be_enabled()
        
        placeholder = input_field.get_attribute("placeholder")
        assert placeholder is not None and len(placeholder) > 0

    def test_TC104_empty_state_message(self, page: Page):
        """TC104: Empty dashboard should show appropriate empty state."""
        # Todo list should be empty initially
        todo_items = page.locator(".todo-list li")
        expect(todo_items).to_have_count(0)


@pytest.mark.dashboard
@pytest.mark.regression
class TestDashboardCRUD:
    """AI-Generated Category: Create, Read, Update, Delete Operations"""

    def test_TC105_create_single_task(self, page: Page):
        """TC105: User should be able to create a new task."""
        page.fill(".new-todo", "Write automated tests")
        page.press(".new-todo", "Enter")
        
        todo_items = page.locator(".todo-list li")
        expect(todo_items).to_have_count(1)
        expect(todo_items.first).to_contain_text("Write automated tests")

    def test_TC106_create_multiple_tasks(self, page: Page):
        """TC106: User should be able to create multiple tasks."""
        tasks = ["Task One", "Task Two", "Task Three"]
        for task in tasks:
            page.fill(".new-todo", task)
            page.press(".new-todo", "Enter")
        
        expect(page.locator(".todo-list li")).to_have_count(3)

    def test_TC107_mark_task_complete(self, page: Page):
        """TC107: User should be able to mark a task as complete."""
        page.fill(".new-todo", "Complete this task")
        page.press(".new-todo", "Enter")
        
        # Click the toggle checkbox
        page.click(".todo-list li .toggle")
        
        # Task should have 'completed' class
        expect(page.locator(".todo-list li")).to_have_class("completed")

    def test_TC108_delete_task(self, page: Page):
        """TC108: User should be able to delete a task."""
        page.fill(".new-todo", "Task to delete")
        page.press(".new-todo", "Enter")
        
        # Hover to reveal delete button
        page.hover(".todo-list li")
        page.click(".todo-list li .destroy")
        
        expect(page.locator(".todo-list li")).to_have_count(0)

    def test_TC109_edit_existing_task(self, page: Page):
        """TC109: User should be able to edit an existing task."""
        page.fill(".new-todo", "Original task name")
        page.press(".new-todo", "Enter")
        
        # Double-click to edit
        page.dblclick(".todo-list li label")
        edit_input = page.locator(".todo-list li .edit")
        edit_input.fill("Updated task name")
        edit_input.press("Enter")
        
        expect(page.locator(".todo-list li label")).to_contain_text("Updated task name")

    def test_TC110_task_count_updates(self, page: Page):
        """TC110: Item count should update as tasks are added/completed."""
        # Add 3 tasks
        for i in range(3):
            page.fill(".new-todo", f"Task {i+1}")
            page.press(".new-todo", "Enter")
        
        count_text = page.locator(".todo-count").inner_text()
        assert "3" in count_text

        # Complete one
        page.click(".todo-list li:first-child .toggle")
        
        count_text = page.locator(".todo-count").inner_text()
        assert "2" in count_text


@pytest.mark.dashboard
@pytest.mark.regression
class TestDashboardFilters:
    """AI-Generated Category: Filter & Navigation Tests"""

    def setup_tasks(self, page: Page):
        """Helper: creates 3 tasks, completes 1."""
        tasks = ["Active Task 1", "Active Task 2", "Completed Task"]
        for task in tasks:
            page.fill(".new-todo", task)
            page.press(".new-todo", "Enter")
        # Complete the last task
        page.locator(".todo-list li").last.locator(".toggle").click()

    def test_TC111_filter_active_tasks(self, page: Page):
        """TC111: 'Active' filter should show only incomplete tasks."""
        self.setup_tasks(page)
        page.click("text=Active")
        # TodoMVC keeps all items in DOM; active = not completed
        active_items = page.locator(".todo-list li:not(.completed)")
        expect(active_items).to_have_count(2)

    def test_TC112_filter_completed_tasks(self, page: Page):
        """TC112: 'Completed' filter should show only completed tasks."""
        self.setup_tasks(page)
        page.click("text=Completed")
        completed_items = page.locator(".todo-list li.completed")
        expect(completed_items).to_have_count(1)
        expect(completed_items.first).to_contain_text("Completed Task")

    def test_TC113_filter_all_tasks(self, page: Page):
        """TC113: 'All' filter should show all tasks."""
        self.setup_tasks(page)
        page.click("text=Active")   # switch away first
        page.click("text=All")      # switch back
        
        expect(page.locator(".todo-list li")).to_have_count(3)

    def test_TC114_clear_completed_tasks(self, page: Page):
        """TC114: 'Clear completed' should remove all completed tasks."""
        self.setup_tasks(page)
        page.click("text=Clear completed")
        
        expect(page.locator(".todo-list li")).to_have_count(2)

    def test_TC115_toggle_all_tasks(self, page: Page):
        """TC115: Toggle-all checkbox should mark all tasks complete."""
        for i in range(3):
            page.fill(".new-todo", f"Task {i+1}")
            page.press(".new-todo", "Enter")
        
        page.click(".toggle-all")
        
        # All should be completed
        completed = page.locator(".todo-list li.completed")
        expect(completed).to_have_count(3)
