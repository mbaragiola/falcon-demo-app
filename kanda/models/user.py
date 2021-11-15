"""
Business and model logic is represented in this module.
"""
from marshmallow import ValidationError


class User:
    """
    Represents a user of our app.
    """

    def __init__(self, first_name, last_name, email, password):
        # Ideally, there should be some validations here.
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @staticmethod
    def validate_name(name):
        if not name.isalpha():
            raise ValidationError("Invalid field type")

    @staticmethod
    def validate_password(password):
        SPECIAL_CHARS = (".", "-", "_", "/", "@", "!")

        # Based on your test cases, it breaks as soon as one fails.

        # Check length.
        if len(password) < 8:
            raise ValidationError("Password must at least be 8 characters")
        if len(password) > 50:
            raise ValidationError("Password must less than 50 characters")

        # Check for letters.
        flag = False
        for c in password:
            if c.isalpha():
                flag = True
                break

        if not flag:
            raise ValidationError("Password must contain at least one letter.")

        # Check for digits.
        flag = False
        for c in password:
            if c.isdigit():
                flag = True
                break

        if not flag:
            raise ValidationError("Password must contain at least one number.")

        # Check for special chars.
        flag = False
        for c in password:
            if c in SPECIAL_CHARS:
                flag = True
                break

        if not flag:
            raise ValidationError("Password must contain at least one special char: %s.", SPECIAL_CHARS)
