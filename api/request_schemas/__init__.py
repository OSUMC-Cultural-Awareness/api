from marshmallow import Schema, fields, ValidationError


class CultureCreateSchema(Schema):
    name = fields.String(required=True)


class CultureUpdateSchema(Schema):
    name = fields.String(required=True)
    general_insights = fields.List(fields.Dict, required=True)
    specialized_insights = fields.List(fields.Dict, required=True)


class AdminLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class AdminRegisterSchema(Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    password_confirmation = fields.String(required=True)


class AdminInviteSchema(Schema):
    email = fields.String(required=True)


class AdminUpdateSchema(Schema):
    email = fields.String(required=True)
    name = fields.String()
    password = fields.String()
    password_confirmation = fields.String()
    superUser = fields.Boolean()


def validate_request_body(schema, body):
    try:
        return schema().load(body)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
