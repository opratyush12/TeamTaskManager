import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    print("Testing Team Task Manager API")
    print("="*60)

    # 1. Register a user
    register_data = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "Admin123!",
        "full_name": "Admin User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response("1. Register User", response)
    user_id = response.json().get("id")

    # 2. Login
    login_data = {
        "email": "admin@example.com",
        "password": "Admin123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("2. Login", response)

    if response.status_code != 200:
        print("Login failed, stopping tests")
        return

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get current user info
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response("3. Get Current User", response)

    # 4. Create a team
    team_data = {
        "name": "Engineering Team",
        "description": "Main engineering team"
    }
    response = requests.post(f"{BASE_URL}/teams", json=team_data, headers=headers)
    print_response("4. Create Team", response)

    if response.status_code != 201:
        print("Team creation failed, stopping tests")
        return

    team_id = response.json()["id"]

    # 5. Get teams
    response = requests.get(f"{BASE_URL}/teams", headers=headers)
    print_response("5. List Teams", response)

    # 6. Create a project
    project_data = {
        "name": "Website Redesign",
        "description": "Redesign company website",
        "team_id": team_id,
        "start_date": datetime.now().date().isoformat(),
        "end_date": (datetime.now() + timedelta(days=30)).date().isoformat()
    }
    response = requests.post(f"{BASE_URL}/projects", json=project_data, headers=headers)
    print_response("6. Create Project", response)

    if response.status_code != 201:
        print("Project creation failed, stopping tests")
        return

    project_id = response.json()["id"]

    # 7. Create tasks
    task1_data = {
        "title": "Design homepage mockup",
        "description": "Create initial design mockup for homepage",
        "project_id": project_id,
        "priority": "high",
        "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task1_data, headers=headers)
    print_response("7a. Create Task 1", response)
    task1_id = response.json()["id"]

    task2_data = {
        "title": "Setup development environment",
        "description": "Configure local dev environment",
        "project_id": project_id,
        "priority": "medium",
        "assigned_to": user_id,
        "due_date": (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task2_data, headers=headers)
    print_response("7b. Create Task 2", response)
    task2_id = response.json()["id"]

    # 8. Update task status
    status_update = {"status": "in_progress"}
    response = requests.put(f"{BASE_URL}/tasks/{task2_id}/status", json=status_update, headers=headers)
    print_response("8. Update Task Status", response)

    # 9. Get all tasks
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    print_response("9. List All Tasks", response)

    # 10. Get tasks by project
    response = requests.get(f"{BASE_URL}/tasks?project_id={project_id}", headers=headers)
    print_response("10. List Tasks by Project", response)

    # 11. Get dashboard overview
    response = requests.get(f"{BASE_URL}/dashboard/overview", headers=headers)
    print_response("11. Dashboard Overview", response)

    # 12. Get dashboard tasks
    response = requests.get(f"{BASE_URL}/dashboard/tasks", headers=headers)
    print_response("12. Dashboard Tasks", response)

    # 13. Get dashboard stats
    response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    print_response("13. Dashboard Stats", response)

    # 14. Update task to done
    task_update = {
        "status": "done",
        "description": "Development environment configured successfully"
    }
    response = requests.put(f"{BASE_URL}/tasks/{task2_id}", json=task_update, headers=headers)
    print_response("14. Complete Task", response)

    # 15. Get project details
    response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
    print_response("15. Get Project Details", response)

    print("\n" + "="*60)
    print("API Testing Complete!")
    print("="*60)
    print(f"\nAPI Documentation: {BASE_URL}/docs")
    print(f"ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Make sure the server is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
