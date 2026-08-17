class SFMShopException(Exception):
    """Базовое исключение для проекта SFMShop"""
    pass
class ValidationError(SFMShopException):
    """Ошибка валидации данных"""
    pass
class NegativePriceError(ValidationError):
    pass
class BusinessLogicError(SFMShopException):
    """Ошибка бизнес-логики"""
    pass
class InsufficientStockError(BusinessLogicError):
    pass
class InvalidOrderError(BusinessLogicError):
    pass
class DatabaseError(SFMShopException):
   pass