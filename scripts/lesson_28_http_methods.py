import requests

# Тело заказа SFMShop, которое отправим на сервер.
order = {"user_id": 1, "product_id": 2, "quantity": 1}

response_post = requests.post("https://httpbin.org/post", json=order)

response_put = requests.put("https://httpbin.org/put", json=order)

response_delete = requests.delete("https://httpbin.org/delete")

response_missing = requests.get("https://httpbin.org/nonexistent")

response_wrong_method = requests.get("https://httpbin.org/post")

print(f"POST /post -> {response_post.status_code}, сервер принял тело: {response_post.json()['json']}")
print(f"PUT /put -> {response_put.status_code}")
print(f"DELETE /delete -> {response_delete.status_code}")
print(f"GET /nonexistent -> {response_missing.status_code} (ресурс не найден)")
print(f"GET /post -> {response_wrong_method.status_code} (метод не разрешён для этого адреса)")
