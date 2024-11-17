from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task = fields.Str(required=True)
    done = fields.Bool(required=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)