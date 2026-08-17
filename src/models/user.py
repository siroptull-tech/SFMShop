
import re
from .exceptions import ValidationError

class User:
    def __init__(self, username, email):
        self.username = username
        self._email = email

    def validate_email(self, email):
        if email is None:
            raise ValidationError("Email не может быть пустым")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Неверный формат email")
        return True

    def set_email(self, email):
        self.validate_email(email)
        self._email = email

    def get_email(self):
        return self._email

    def create(self):
        return f"Пользователь: {self.username}, Email: {self._email}"