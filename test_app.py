import unittest
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

BASE_URL = "http://127.0.0.1:5000/tasks/"  # Adjust if your Flask app runs elsewhere
AUTH = (os.getenv("USERNAME"), os.getenv("PASSWORD"))  # Ensure this matches your app's environment variables

class TaskManagementApiTest(unittest.TestCase):

    def test_create_task_success(self):
        """Test creating a new task"""
        task_data = {
            "description": "Test Task2",
            "due_date": "2025-03-10",
            "status": "active"
        }
        response = requests.post(BASE_URL, json=task_data, auth=AUTH)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_get_all_tasks(self):
        """Test retrieving all tasks"""
        response = requests.get(BASE_URL, json={}, auth=AUTH)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_task_by_id(self):
        """Test retrieving a specific task"""
        # First, create a task
        task_data = {
            "description": "Task to fetch",
            "due_date": "2025-03-25",
            "status": "active"
        }
        create_response = requests.post(BASE_URL, json=task_data, auth=AUTH)
        task_id = create_response.json()["id"]

        # Fetch the task by ID
        response = requests.get(f"{BASE_URL}{task_id}", auth=AUTH)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], task_id)

    def test_update_task(self):
        """Test updating a task"""
        # First, create a task
        task_data = {
            "description": "Task to update",
            "due_date": "2025-03-10",
            "status": "active"
        }
        create_response = requests.post(BASE_URL, json=task_data, auth=AUTH)
        task_id = create_response.json()["id"]

        # Update the task
        updated_task = {
            "description": "Updated Task",
            "due_date": "2025-03-15",
            "status": "completed"
        }
        response = requests.put(f"{BASE_URL}{task_id}", json=updated_task, auth=AUTH)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "Updated Task")

    def test_delete_task(self):
        """Test deleting a task"""
        # First, create a task
        task_data = {
            "description": "Task to delete",
            "due_date": "2025-03-10",
            "status": "active"
        }
        create_response = requests.post(BASE_URL, json=task_data, auth=AUTH)
        task_id = create_response.json()["id"]

        # Delete the task
        response = requests.delete(f"{BASE_URL}{task_id}", auth=AUTH)
        self.assertEqual(response.status_code, 204)

        # Ensure it's deleted
        response = requests.get(f"{BASE_URL}{task_id}", auth=AUTH)
        self.assertEqual(response.status_code, 404)

    def test_create_task_duplicate(self):
        """Test that creating a duplicate task returns a 409 Conflict response"""
        task_data = {
            "description": "Test Task",
            "due_date": "2025-03-28",
            "status": "active"
        }

        # First request: Create task
        response1 = requests.post(BASE_URL, json=task_data, auth=AUTH)
        self.assertEqual(response1.status_code, 201)  # Ensure first task is created

        # Second request: Attempt to create the same task again
        response2 = requests.post(BASE_URL, json=task_data, auth=AUTH)
        self.assertEqual(response2.status_code, 409)  # Expecting 409 Conflict


if __name__ == '__main__':
    unittest.main()
