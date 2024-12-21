from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["JWT_SECRET_KEY"] = "your_secret_key"
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Import models and schemas
from models import Task, User
from schemas import TaskSchema, UserSchema

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Routes

# User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully"}

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.username)
        return {"access_token": token}
    return {"error": "Invalid credentials"}, 401

# Get all tasks (with pagination)
@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    tasks = Task.query.paginate(page=page, per_page=per_page, error_out=False)
    return tasks_schema.jsonify(tasks.items)

# Create a new task
@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.json
    new_task = Task(name=data["name"], description=data.get("description", ""))
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# Search tasks
@app.route("/tasks/search", methods=["GET"])
@jwt_required()
def search_tasks():
    query = request.args.get("q", "")
    tasks = Task.query.filter(Task.name.ilike(f"%{query}%")).all()
    return tasks_schema.jsonify(tasks)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(400)
def bad_request(error):
    return {"error": "Bad request"}, 400

if __name__ == "__main__":
    app.run(debug=True)
