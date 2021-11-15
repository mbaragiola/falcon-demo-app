"""
Schema input/output and validations are found here.
"""
from marshmallow import Schema, fields, post_load

from ..models.user import User


class UserSchema(Schema):
    """
    Schema for models.User
    """

    first_name = fields.Str(required=True, validate=User.validate_name)
    last_name = fields.Str(required=True, validate=User.validate_name)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=User.validate_password)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
