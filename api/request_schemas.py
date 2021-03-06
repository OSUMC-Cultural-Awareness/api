"""Module for request body schemas and validation function."""
from typing import Any, Dict, Optional, Union

from marshmallow import Schema, ValidationError, fields, validate


class InsightSchema(Schema):
    """Structure of insights.

    Format:
    {
      "summary": "summary",
      "information": "text",
      "source": {
        "data": "www.example.com",
        "type": "link"
      }
    }
    """

    summary = fields.String(required=True)
    information = fields.String(required=True)
    source = fields.Dict(keys=fields.String(), values=fields.String(), required=True)


class FeedbackSchema(Schema):
    """POST /api/v1/feedback.

    Format:
    {
      "feedback": "..."
    }
    """

    feedback = fields.String(validate=validate.Length(min=1, max=300), required=True)


class CultureCreateSchema(Schema):
    """POST /api/v1/cultures.

    Format:
    {
      "name": "culture"
    }
    """

    name = fields.String(required=True)


class CultureUpdateSchema(Schema):
    """PUT /api/v1/cultures/<name>.

    Format:
    {
      "name": "Culture",
      "general_insights": [],
      "specialized_insights": {"type": [InsightSchema...]}
    }
    """

    name = fields.String(required=True)
    general_insights = fields.List(fields.Nested(InsightSchema()), required=True)
    specialized_insights = fields.Dict(
        keys=fields.String(),
        values=fields.List(fields.Nested(InsightSchema()), required=True),
    )


class AdminLoginSchema(Schema):
    """POST /api/v1/login.

    Format:
    {
      "email": "test@gmail.com",
      "password": "password"
    }
    """

    email = fields.Email(required=True)
    password = fields.String(required=True)


class AdminRegisterSchema(Schema):
    """POST /api/v1/register.

    Format:
    {
      "name": "name",
      "email": "test@gmail.com",
      "password": "password",
      "password_confirmation": "password"
    }
    """

    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    password_confirmation = fields.String(required=True)


class AdminEmailSchema(Schema):
    """POST /api/v1/admins/invite and /api/v1/admins/recover.

    Format:
    {
      "email": "test@gmail.com"
    }
    """

    email = fields.Email(required=True)


class AdminUpdateSchema(Schema):
    """PUT /api/v1/admins/<email>.

    Format:
    {
      "name": "name",
    }
    """

    name = fields.String()


def validate_request_body(schema, body: Dict) -> Union[str, Dict[str, Any]]:
    """Validates a request body using the corresponding request schema."""
    try:
        return schema().load(body)
    except ValidationError as err:
        return (
            f"Error: Request body containing `{err.valid_data}` invalid: {err.messages}"
        )
