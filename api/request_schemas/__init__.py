from marshmallow import Schema, fields, ValidationError


class CultureCreateSchema(Schema):
    """
    POST /vi/culture
    """

    name = fields.String(required=True)


class CultureUpdateSchema(Schema):
    """
    PUT /v1/culture/<name>
    """

    name = fields.String(required=True)
    general_insights = fields.List(fields.Dict, required=True)
    specialized_insights = fields.List(fields.Dict, required=True)


class AdminLoginSchema(Schema):
    """
    POST /v1/login
    """

    email = fields.String(required=True)
    password = fields.String(required=True)


class AdminRegisterSchema(Schema):
    """
    POST /v1/register
    """

    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    password_confirmation = fields.String(required=True)


class AdminInviteSchema(Schema):
    """
    POST /v1/admin/invite
    """

    email = fields.String(required=True)


class AdminUpdateSchema(Schema):
    """
    PUT /v1/admin/<email>
    """

    email = fields.String(required=True)
    name = fields.String()
    password = fields.String()
    password_confirmation = fields.String()
    superUser = fields.Boolean()


def validate_request_body(schema, body):
    """
    Validates a request body using the corresponding request schema
    """
    try:
        return schema().load(body)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
