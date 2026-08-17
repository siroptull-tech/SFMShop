

def calculate_discount(price, discount_rate):
    return price * discount_rate

def calculate_delivery(weight, distance=0):
    return 100 + weight * 10 + distance * 5

def calculate_final_price(price, discount, delivery):
    return price - discount + delivery

