from fastapi import status

def test_create_customer(client):
    response = client.post("/customers",
    json={
        "name":"jhon doe",
        "email":"jhon@example.com",
        "age": 33
    })

    assert response.status_code == status.HTTP_201_CREATED

def test_get_customer(client):
    response = client.post("/customers",
    json={
        "name":"jhon doe",
        "email":"jhon@example.com",
        "age": 33
    })

    assert response.status_code == status.HTTP_201_CREATED
    customer_id = response.json()["id"]
    response_get = client.get(f"/customers/{customer_id}")
    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json()["name"] == "jhon doe"