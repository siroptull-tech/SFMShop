import json


class MiniRouter:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def dispatch(self, method, path):
        parts = path.strip("/").split("/")

        for (route_method, route_path), handler in self.routes.items():
            if route_method != method:
                continue

            route_parts = route_path.strip("/").split("/")
            if len(route_parts) != len(parts):
                continue

            params = {}
            match = True
            for route_part, part in zip(route_parts, parts):
                if route_part.startswith("{") and route_part.endswith("}"):
                    params[route_part[1:-1]] = part
                elif route_part != part:
                    match = False
                    break

            if match:
                result = handler(**params) if params else handler()
                if isinstance(result, tuple):
                    status, body = result
                else:
                    status, body = 200, result
                return status, json.dumps(body, ensure_ascii=False)

        return 404, json.dumps({"error": "Not Found"}, ensure_ascii=False)


PRODUCTS = {
    1: {"id": 1, "name": "Ноутбук", "price": 50000},
    2: {"id": 2, "name": "Мышь", "price": 1500},
    3: {"id": 3, "name": "Клавиатура", "price": 3000},
}


def get_products():
    return list(PRODUCTS.values())


def get_product(product_id):
    product_id = int(product_id)
    if product_id not in PRODUCTS:
        return 404, {"error": "Товар не найден"}
    return PRODUCTS[product_id]


router = MiniRouter()
router.add_route("GET", "/products", get_products)
router.add_route("GET", "/products/{product_id}", get_product)

requests = [
    ("GET", "/products"),
    ("GET", "/products/2"),
    ("GET", "/products/99"),
    ("POST", "/products"),
]

for method, path in requests:
    status, body = router.dispatch(method, path)
    print(f"{method} {path} -> {status} {body}")
