
from .exceptions import InsufficientStockError, ValidationError
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        
    def set_price(self, price):
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self.price = price
        
    def sell(self, amount):
        if amount > self.quantity:
            raise InsufficientStockError(f"Товара недостаточно. На складе: {self.quantity}, требуется: {amount}")
        self.quantity -= amount
        
    def get_total_price(self):
        return round(self.price * self.quantity * 0.9, 2)
    
    def get_category(self):
        if self.price >= 30000:
            return "Премиум"
        if self.price >= 5000:
            return "Средний сегмент"
        return "Эконом"

    def __lt__(self, other):
        if isinstance(other, Product):
            return self.price < other.price
    
    def __eq__(self, value):
        if isinstance(value, Product):
            return self.price == value.price and self.name == value.name
        return False
        
    def __str__(self):
        return f"Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}"
        
    def __repr__(self):
        return f"Product('{self.name}', {self.price}, {self.quantity})"
    
