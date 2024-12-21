from marshmallow import Schema, fields

#This file handles input validation and serialization using Marshmallow.
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task = fields.Str(required=True)
    done = fields.Bool(required=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)