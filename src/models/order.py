
from .exceptions import InvalidOrderError, BusinessLogicError
from .product import Product

class Order:
    def __init__(self, user=None, products=None):
        if products is None:
            products = []
        self.products = products
        self.user = user
    
    def add_product(self, product):
        if not isinstance(product, Product):
            raise InvalidOrderError("Заказ невалиден: добавлен невалидный товар")
        self.products.append(product)
    
    def create_order(self):
        if not self.products:
            raise BusinessLogicError("Заказ невалиден: пустой список товаров")
        return f"Заказ создан для пользователя {self.user.username} с {len(self.products)} товарами."
    
    def calculate_total(self,):
        total = 0
        for product in self.products:
            total += product.price * product.quantity
        return total
    
    def __str__(self):
        return f"Заказ пользователя {self.user.username} на сумму {str(self.calculate_total())} руб."
       
       