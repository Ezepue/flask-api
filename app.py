from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["JWT_SECRET_KEY"] = "your_secret_key"

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Import models and schemas
    from models import Task, User
    from schemas import TaskSchema, UserSchema

    # Routes

    @app.route("/register", methods=["POST"])
    def register():
        data = request.json
        new_user = User(username=data["username"], password=data["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            token = create_access_token(identity=user.username)
            return jsonify({"access_token": token}), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def get_tasks():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        tasks = Task.query.paginate(page=page, per_page=per_page, error_out=False)
        tasks_schema = TaskSchema(many=True)
        return tasks_schema.jsonify(tasks.items)

    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        data = request.json
        new_task = Task(name=data["name"], description=data.get("description", ""))
        db.session.add(new_task)
        db.session.commit()
        task_schema = TaskSchema()
        return task_schema.jsonify(new_task), 201

    @app.route("/tasks/search", methods=["GET"])
    @jwt_required()
    def search_tasks():
        query = request.args.get("q", "")
        tasks = Task.query.filter(Task.name.ilike(f"%{query}%")).all()
        tasks_schema = TaskSchema(many=True)
        return tasks_schema.jsonify(tasks)

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
