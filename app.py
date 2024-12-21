from flask import Flask, request, jsonify
from models import db, Task
from schemas import task_schema, tasks_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
#This file brings everything together.
# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return jsonify(message="Welcome to Ozmanthus's To-Do API!")

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks)

# Get a single task by ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({"message": "Task not found"}), 404
    return task_schema.jsonify(task)

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    try:
        new_task = task_schema.load(data)
        task = Task(task=new_task["task"], done=new_task["done"])
        db.session.add(task)
        db.session.commit()
        return task_schema.jsonify(task), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    try:
        updated_data = task_schema.load(data)
        task.task = updated_data["task"]
        task.done = updated_data["done"]
        db.session.commit()
        return task_schema.jsonify(task)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
