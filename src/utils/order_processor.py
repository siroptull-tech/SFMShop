
def load_orders_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            orders = file.readlines()
            orders = [o.strip() for o in orders]
            return orders
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []
    
def calculate_order_total(price, discount_rate):
    total_price = price * (1 - discount_rate)
    return round(total_price, 2)

def get_discount_by_total(total):
    if total <= 0:
        return 0
    if total > 10000:
        return 0.15
    elif total > 5000:
        return 0.1
    else:
        return 0.05
         
def process_orders(orders_data):
    processed_orders = []
    for order in orders_data:
        order_details = order.split(':')
        if len(order_details) != 4:
            print(f"Неверный формат заказа!: {order}")
            continue
        try:
            get_discount = get_discount_by_total(int(order_details[1]))
            order_total = calculate_order_total(int(order_details[1]), get_discount)
        except (ValueError, IndexError):
            print(f"Неверный формат заказа!: {order}")
            continue
        order_dict = {
            "order_id": order_details[0],
            "total": order_total,
            "status": order_details[2],
            "user": order_details[3]
        }
        processed_orders.append(order_dict)
    return processed_orders
         
def analyze_orders(processed_orders):
    stats = {
        "total_orders": 0,
        "total_sum": 0,
        "by_status": {},
        "unique_users": set()
        }
    for order in processed_orders:
        stats["total_orders"] += 1
        stats["total_sum"] += order["total"]
        stats["by_status"][order["status"]] = stats["by_status"].get(order["status"], 0) + 1
        stats["unique_users"].add(order["user"])
    
    return {
        "total_orders": stats["total_orders"],
        "total_sum": stats["total_sum"],
        "by_status": stats["by_status"],
        "unique_users": list(stats["unique_users"]),
    }

def process_order_file(input_file, output_file):
    orders = load_orders_from_file(input_file)
    processed_orders = process_orders(orders)
    analyze_data = analyze_orders(processed_orders)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        status_str = ', '.join([f"{status}: {count}" for status, count in analyze_data['by_status'].items()])
        file.write(f"Обработано заказов: {analyze_data['total_orders']}\n"
                   f"Общая сумма: {analyze_data['total_sum']} руб.\n"
                   f"По статусам: {status_str}\n"
                   f"Уникальных пользователей: {len(analyze_data['unique_users'])}")
        


