from app import ma
from models import Task, User

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
