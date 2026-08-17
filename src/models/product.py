
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
            return self.price * self.quantity

    def check_stock(self, required_quantity):
        if self.quantity >= required_quantity:
            return f"Товар '{self.name}' в наличии: {self.quantity} шт."
        return f"Товара '{self.name}' недостаточно: в наличии {self.quantity} шт., требуется {required_quantity} шт."

    def update_stock(self, amount):
        if amount < 0 and abs(amount) > self.quantity:
            raise InsufficientStockError(f"Нельзя списать {abs(amount)} шт., на складе только {self.quantity} шт.")
        self.quantity += amount
        return f"Остаток товара '{self.name}' обновлён: {self.quantity} шт."
    
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
    
