"""
Module for request body schemas and validation function
"""
from typing import Any, Dict, Union
from marshmallow import Schema, fields, ValidationError


class InsightSchema(Schema):
    """
    strucure of insights
    """

    summary = fields.String(required=True)
    information = fields.String(required=True)
    source = fields.Dict(keys=fields.String(), values=fields.String(), required=True)


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
    general_insights = fields.List(fields.Nested(InsightSchema()), required=True)
    specialized_insights = fields.List(fields.Nested(InsightSchema()), required=True)


class AdminLoginSchema(Schema):
    """
    POST /v1/login
    """

    email = fields.Email(required=True)
    password = fields.String(required=True)


class AdminRegisterSchema(Schema):
    """
    POST /v1/register
    """

    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    password_confirmation = fields.String(required=True)


class AdminInviteSchema(Schema):
    """
    POST /v1/admin/invite
    """

    email = fields.Email(required=True)


class AdminUpdateSchema(Schema):
    """
    PUT /v1/admin/<email>
    """

    email = fields.Email(required=True)
    name = fields.String()
    password = fields.String()
    password_confirmation = fields.String()
    superUser = fields.Boolean()


def validate_request_body(schema, body: Dict) -> Union[str, Dict[str, Any]]:
    """
    Validates a request body using the corresponding request schema
    """
    try:
        return schema().load(body)
    except ValidationError as err:
        return (
            f"Error: Request body containing `{err.valid_data}` invalid: {err.messages}"
        )
