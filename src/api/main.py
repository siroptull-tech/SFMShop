from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

from src.database.connection import (
    connect_to_db,
    count_products,
    get_products_page,
    get_product_by_id,
    update_product as update_product_db,
    delete_product as delete_product_db,
    get_user_by_id,
    create_order as create_order_db,
)
from src.models.product import Product
from src.models.user import User
from src.models.order import Order


conn = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global conn
    conn = connect_to_db()
    yield
    if conn:
        conn.close()


app = FastAPI(lifespan=lifespan)


USERS = {
    1: {"id": 1, "name": "Иван", "email": "ivan@test.ru"},
    2: {"id": 2, "name": "Мария", "email": "maria@test.ru"},
}


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class UserCreate(BaseModel):
    name: str
    email: str


class ProductUpdate(BaseModel):
    name: str
    price: float
    quantity: int


@app.get("/products")
def get_products(limit: int = 10, offset: int = 0):
    try:
        total = count_products(conn)
        rows = get_products_page(conn, limit, offset)

        products = []
        for row in rows:
            product = Product(row[1], row[2], row[3])  # name, price, quantity
            product.id = row[0]
            products.append(product.__dict__)

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "products": products,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        row = get_product_by_id(conn, product_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        product = Product(row[1], row[2], row[3])
        product.id = row[0]
        return product.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: ProductUpdate):
    try:
        if get_product_by_id(conn, product_id) is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        update_product_db(conn, product_id, product_data.name, product_data.price, product_data.quantity)

        product = Product(product_data.name, product_data.price, product_data.quantity)
        product.id = product_id
        return product.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        deleted = delete_product_db(conn, product_id)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Товар не найден")
        return {"message": "Товар удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    try:
        user_row = get_user_by_id(conn, order.user_id)
        if user_row is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        product_row = get_product_by_id(conn, order.product_id)
        if product_row is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        user_obj = User(user_row["name"], user_row["email"])
        product_obj = Product(product_row[1], product_row[2], order.quantity)

        order_obj = Order(user=user_obj, products=[product_obj])
        total = order_obj.calculate_total()

        order_id = create_order_db(conn, order.user_id, total)
        if order_id is None:
            raise HTTPException(status_code=500, detail="Не удалось сохранить заказ")

        return {
            "id": order_id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total": total,
            "message": "Заказ создан",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def get_users():
    return list(USERS.values())


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return USERS[user_id]


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    new_id = max(USERS.keys(), default=0) + 1
    new_user = {"id": new_id, "name": user.name, "email": user.email}
    USERS[new_id] = new_user
    return new_user


def test_api():
    with TestClient(app) as client:
        response = client.get("/products")
        assert response.status_code == 200
        print("GET /products: OK")

        response = client.get("/products?limit=2&offset=1")
        assert response.status_code == 200
        assert len(response.json()["products"]) == 2
        print("GET /products?limit=2&offset=1: OK")

        response = client.get("/products/1")
        assert response.status_code == 200
        print("GET /products/1: OK")

        response = client.get("/products/999")
        assert response.status_code == 404
        print("GET /products/999: OK (404)")

        response = client.put("/products/1", json={"name": "Ноутбук", "price": 51000, "quantity": 9})
        assert response.status_code == 200
        print("PUT /products/1: OK")

        response = client.post("/orders", json={"user_id": 1, "product_id": 2, "quantity": 1})
        assert response.status_code == 201
        print("POST /orders: OK")

        response = client.delete("/products/999")
        assert response.status_code == 404
        print("DELETE /products/999: OK (404)")


if __name__ == "__main__":
    test_api()
