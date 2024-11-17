from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite=///tasks.db'
db = SQLAlchemy(app)

# Define Task Model
class TaskModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    
# Create the database
with app.app_context():
    db.create_all

# Define Task Schema
class TaskSchma(Schema):
    id = fields.Int()
    task = fields.Str(required=True)
    done = fields.Bool(required=True)
    
task_schema = TaskSchma()
task = []


#Home Route
@app.route('/')
def home():
    return jsonify(message="Welcome to Ozmanthus' To-Do API!")

#Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(to_do_list)


#Validate Input Data
@app.route('/api/tasks', methods=['POST'])
def add_tasks():
    try:
        new_task = task_schema.load(request.get_json())
        new_task["id"] = len(to_do_list) + 1
        to_do_list.append(new_task)
        return jsonify(new_task), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# Update a Task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = request.get_json()
    for task in to_do_list:
        if task["id"] == task_id:
            task["task"] = updated_task.get("task", task["task"])
            task["done"] = updated_task.get("done", task["done"])
            return jsonify(task)
    return jsonify({"message": "Task not found"}), 404
    
# Delete a Task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global to_do_list
    to_do_list = [task for task in to_do_list if task["id"] != task_id]
    return jsonify({"message": "Task Deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)