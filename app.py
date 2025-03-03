from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_httpauth import HTTPBasicAuth
import logging
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app, title='Task Management API', version='1.0', description='A simple Task Management API')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve credentials from environment variables
USER_CREDENTIALS = os.getenv("USER_CREDENTIALS")
if not USER_CREDENTIALS:
    raise ValueError("USER_CREDENTIALS environment variable must be set")

users = dict(cred.split(":") for cred in USER_CREDENTIALS.split(","))


tasks = []  # In-memory storage for tasks


@auth.verify_password
def verify(username, password):
    if users.get(username) == password:
        return username
    return None


ns = api.namespace('tasks', description='Task operations')

task_model = api.model('Task', {
    'id': fields.String(readOnly=True, description='The task identifier'),
    'description': fields.String(required=True, description='Task description'),
    'due_date': fields.Date(required=True, description='Due date (YYYY-MM-DD)'),
    'status': fields.String(required=True, description='Task status', enum=['active', 'completed'])
})


def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)


@ns.route('/', strict_slashes=False)
class TaskList(Resource):
    """Shows a list of all tasks"""

    @auth.login_required
    @ns.marshal_list_with(task_model)
    def get(self):
        """Get all tasks"""
        logging.info("Fetching all tasks")
        return tasks

    @auth.login_required
    @ns.expect(task_model, validate=True)
    @ns.marshal_with(task_model, code=201)
    def post(self):
        """Create a new task"""
        new_task = api.payload
        new_task['id'] = str(uuid.uuid4())

        # Check for duplicate task (same description, due date, and status)
        if any(task['description'] == new_task['description'] and
               str(task['due_date']) == new_task['due_date'] and
               task['status'] == new_task['status'] for task in tasks):
            logging.warning(f"Duplicate task detected: {new_task}")
            api.abort(409, "Conflict: Task with the same description, due date, and status already exists.")
        try:
            new_task['due_date'] = datetime.strptime(new_task['due_date'], "%Y-%m-%d").date()
        except ValueError:
            logging.error("Invalid date format. Expected YYYY-MM-DD.")
            api.abort(400, "Invalid date format. Expected YYYY-MM-DD.")
        tasks.append(new_task)
        logging.info(f"Task created: {new_task}")
        return new_task, 201


@ns.route('/<string:task_id>')
@ns.response(404, 'Task not found')
class Task(Resource):
    """Handles single task operations"""

    @auth.login_required
    @ns.marshal_with(task_model)
    def get(self, task_id):
        """Get a specific task by ID"""
        task = find_task(task_id)
        if task is None:
            logging.warning(f"Task {task_id} not found")
            api.abort(404, 'Task not found')
        logging.info(f"Fetching task {task_id}")
        return task

    @auth.login_required
    @ns.expect(task_model)
    @ns.marshal_with(task_model)
    def put(self, task_id):
        """Update an existing task"""
        task = find_task(task_id)
        if task is None:
            logging.warning(f"Task {task_id} not found for update")
            api.abort(404, 'Task not found')
        data = request.json
        if 'due_date' in data:
            try:
                data['due_date'] = datetime.strptime(data['due_date'], "%Y-%m-%d").date()
            except ValueError:
                logging.error("Invalid date format. Expected YYYY-MM-DD.")
                api.abort(400, "Invalid date format. Expected YYYY-MM-DD.")
        task.update(data)
        logging.info(f"Task {task_id} updated: {data}")
        return task

    @auth.login_required
    @ns.response(204, 'Task deleted')
    def delete(self, task_id):
        """Delete a task"""
        global tasks
        if not find_task(task_id):
            logging.warning(f"Task {task_id} not found for deletion")
            api.abort(404, 'Task not found')
        tasks = [task for task in tasks if task['id'] != task_id]
        logging.info(f"Task {task_id} deleted")
        return '', 204


if __name__ == '__main__':
    app.run(debug=False)

