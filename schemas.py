from marshmallow import Schema, fields

class ResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True)
    response = fields.Str(dump_only=True)
    response_type = fields.Str(dump_only=True)