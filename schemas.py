from marshmallow import Schema, fields, ValidationError

# Define Task Schema
class TaskSchma(Schema):
    id = fields.Int(dump_only=True)
    task = fields.Str(required=True)
    done = fields.Bool(required=True)
    
task_schema = TaskSchma()
tasks_schema = TaskSchma(many=True)
