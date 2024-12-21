from flask import Blueprint, jsonify, request
from . import db
from .models import Task, User

# Define a Blueprint for routes
bp = Blueprint('main', __name__)

# Example route to get all tasks
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.title for task in tasks])

# Example route to add a task
@bp.route('/tasks', methods=['POST'])
def add_task():
    title = request.json.get('title')
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"}), 201
