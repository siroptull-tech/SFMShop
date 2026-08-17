
from .exceptions import ValidationError

class User:
    def __init__(self, username, email):
        self.username = username
        self._email = email
        
    def set_email(self, email):
        if email is None or "@" not in email:
            raise ValidationError("Неверный формат email")
        self._email = email
        
    def get_email(self):
        return self._email    
        
    def create(self):
        return f"Пользователь: {self.username}, Email: {self._email}"

    def get_info(self):
        return f"[User] {self.username} | {self._email}"