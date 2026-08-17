
class Payment:
    def __init__(self, amount):
        self.amount = amount

    def process_payment(self):
        raise NotImplementedError("Метод должен быть переопределен")
    
class CardPayment(Payment):
    def __init__(self, amount, card_number):
        self.__card_number = card_number
        super().__init__(amount)
    def process_payment(self):
        return f"Оплата картой {self.__card_number[-4:]}: {self.amount} руб."
    
class PayPalPayment(Payment):
    def __init__(self, amount, email):
        self.email = email
        super().__init__(amount)
    def process_payment(self):
        return f"Оплата PayPal ({self.email}): {self.amount} руб."
    