"""
REST API Module Tests
=====================
Test cases AI-generated using GPT-4o-mini.
Prompt: "Generate comprehensive REST API test cases for a JSONPlaceholder-like API
covering CRUD operations, status codes, schema validation, auth, and edge cases."

Target: https://jsonplaceholder.typicode.com (Public REST API - perfect for demos)
"""

import pytest
import requests
import json


BASE_URL = "https://jsonplaceholder.typicode.com"

# Schema definitions (AI-suggested based on API structure)
POST_SCHEMA = {"userId", "id", "title", "body"}
USER_SCHEMA = {"id", "name", "username", "email", "address", "phone", "website", "company"}
COMMENT_SCHEMA = {"postId", "id", "name", "email", "body"}


def validate_schema(data: dict, required_keys: set, test_name: str):
    """Helper: Validates response body contains required keys."""
    missing = required_keys - set(data.keys())
    assert not missing, f"[{test_name}] Missing keys: {missing}"


@pytest.mark.api
@pytest.mark.smoke
class TestAPIGetRequests:
    """AI-Generated Category: GET Request Tests"""

    def test_TC201_get_all_posts_returns_200(self):
        """TC201: GET /posts should return 200 with a list."""
        response = requests.get(f"{BASE_URL}/posts")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 100  # JSONPlaceholder always has 100 posts

    def test_TC202_get_single_post_returns_200(self):
        """TC202: GET /posts/1 should return a valid post object."""
        response = requests.get(f"{BASE_URL}/posts/1")
        
        assert response.status_code == 200
        data = response.json()
        validate_schema(data, POST_SCHEMA, "TC202")
        assert data["id"] == 1

    def test_TC203_get_nonexistent_post_returns_404(self):
        """TC203: GET /posts/99999 should return 404."""
        response = requests.get(f"{BASE_URL}/posts/99999")
        assert response.status_code == 404

    def test_TC204_get_all_users_returns_correct_schema(self):
        """TC204: GET /users should return users with correct schema."""
        response = requests.get(f"{BASE_URL}/users")
        
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 10
        validate_schema(users[0], USER_SCHEMA, "TC204")

    def test_TC205_get_posts_by_user_filter(self):
        """TC205: GET /posts?userId=1 should return only user 1's posts."""
        response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
        
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts), "Filter returned posts from other users"

    def test_TC206_response_content_type_is_json(self):
        """TC206: API responses should have application/json content type."""
        response = requests.get(f"{BASE_URL}/posts/1")
        
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type

    def test_TC207_get_comments_for_post(self):
        """TC207: GET /posts/1/comments should return comments with correct schema."""
        response = requests.get(f"{BASE_URL}/posts/1/comments")
        
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        validate_schema(comments[0], COMMENT_SCHEMA, "TC207")
        assert all(c["postId"] == 1 for c in comments)

    def test_TC208_response_time_under_threshold(self):
        """TC208: API response time should be under 3 seconds."""
        import time
        start = time.time()
        response = requests.get(f"{BASE_URL}/posts")
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 3.0, f"Response too slow: {elapsed:.2f}s"


@pytest.mark.api
@pytest.mark.regression
class TestAPIPostRequests:
    """AI-Generated Category: POST / Create Operation Tests"""

    def test_TC209_create_post_returns_201(self):
        """TC209: POST /posts should create a resource and return 201."""
        payload = {
            "title": "TestMu AI Hackathon Post",
            "body": "This post was created by an automated test.",
            "userId": 1
        }
        response = requests.post(f"{BASE_URL}/posts", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert "id" in data  # Server assigned an ID

    def test_TC210_create_post_with_empty_body(self):
        """TC210: POST with empty body should still return a response (JSONPlaceholder is lenient)."""
        response = requests.post(f"{BASE_URL}/posts", json={})
        
        # JSONPlaceholder accepts empty but real APIs should validate
        assert response.status_code in [201, 400, 422]

    def test_TC211_create_post_returns_correct_content_type(self):
        """TC211: POST response should have JSON content type."""
        response = requests.post(f"{BASE_URL}/posts", json={"title": "test", "userId": 1})
        
        assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.api
@pytest.mark.regression
class TestAPIPutPatchRequests:
    """AI-Generated Category: PUT / PATCH / Update Tests"""

    def test_TC212_put_updates_entire_resource(self):
        """TC212: PUT /posts/1 should fully update the resource."""
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1
        }
        response = requests.put(f"{BASE_URL}/posts/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    def test_TC213_patch_updates_partial_resource(self):
        """TC213: PATCH /posts/1 should update only specified fields."""
        response = requests.patch(
            f"{BASE_URL}/posts/1",
            json={"title": "Patched Title Only"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title Only"
        # Other fields should still exist
        assert "body" in data


@pytest.mark.api
@pytest.mark.regression
class TestAPIDeleteRequests:
    """AI-Generated Category: DELETE Operation Tests"""

    def test_TC214_delete_post_returns_200(self):
        """TC214: DELETE /posts/1 should return 200."""
        response = requests.delete(f"{BASE_URL}/posts/1")
        assert response.status_code == 200

    def test_TC215_delete_nonexistent_post(self):
        """TC215: DELETE on non-existent resource."""
        response = requests.delete(f"{BASE_URL}/posts/99999")
        # JSONPlaceholder returns 200 even for non-existent; real APIs return 404
        assert response.status_code in [200, 404]


@pytest.mark.api
@pytest.mark.regression
class TestAPIEdgeCases:
    """AI-Generated Category: Edge Cases & Validation"""

    def test_TC216_invalid_endpoint_returns_404(self):
        """TC216: Non-existent endpoint should return 404."""
        response = requests.get(f"{BASE_URL}/nonexistentendpoint")
        assert response.status_code == 404

    def test_TC217_response_is_valid_json(self):
        """TC217: All responses should be parseable JSON."""
        response = requests.get(f"{BASE_URL}/posts/1")
        
        try:
            data = response.json()
            assert data is not None
        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")

    def test_TC218_get_todos_schema_validation(self):
        """TC218: GET /todos should return items with correct schema."""
        response = requests.get(f"{BASE_URL}/todos/1")
        
        assert response.status_code == 200
        data = response.json()
        required = {"userId", "id", "title", "completed"}
        validate_schema(data, required, "TC218")
        assert isinstance(data["completed"], bool)

    def test_TC219_pagination_via_query_params(self):
        """TC219: API should support limiting results via _limit param."""
        response = requests.get(f"{BASE_URL}/posts", params={"_limit": 5})
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_TC220_get_nested_resource(self):
        """TC220: Nested resource /users/1/posts should return user's posts."""
        response = requests.get(f"{BASE_URL}/users/1/posts")
        
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts)
