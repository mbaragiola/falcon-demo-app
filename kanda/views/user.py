"""
Views and endpoints logic goes here.
"""
import json
import falcon
from marshmallow import ValidationError

from ..schemas.user import UserSchema


class UserSignup:
    """
    Handles user signups.
    If there's a validation error, returns 400 with corresponding message.
    If not, returns a blank 201.
    """

    def on_post(self, req, resp):
        schema = UserSchema()
        try:
            schema.load(req.params)
        except ValidationError as err:
            msg = {
                "error": "Bad request",
                "field_errors": err.messages
            }
            resp.text = json.dumps(msg)
            resp.status = falcon.HTTP_400
        else:
            resp.text = json.dumps({})
            resp.status = falcon.HTTP_201
