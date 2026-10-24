from fastapi.testclient import TestClient


def test_create_and_get_item(client: TestClient) -> None:
    created = client.post("/api/items", json={"name": "Lion", "description": "Big cat"})
    assert created.status_code == 201
    item = created.json()
    assert item["name"] == "Lion"

    fetched = client.get(f"/api/items/{item['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == item


def test_list_items(client: TestClient) -> None:
    client.post("/api/items", json={"name": "Lion"})
    client.post("/api/items", json={"name": "Tiger"})

    response = client.get("/api/items")
    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Lion", "Tiger"]


def test_update_item(client: TestClient) -> None:
    item_id = client.post("/api/items", json={"name": "Lion"}).json()["id"]

    response = client.patch(f"/api/items/{item_id}", json={"description": "King"})
    assert response.status_code == 200
    assert response.json()["name"] == "Lion"
    assert response.json()["description"] == "King"


def test_delete_item(client: TestClient) -> None:
    item_id = client.post("/api/items", json={"name": "Lion"}).json()["id"]

    assert client.delete(f"/api/items/{item_id}").status_code == 204
    assert client.get(f"/api/items/{item_id}").status_code == 404


def test_missing_item_returns_404(client: TestClient) -> None:
    response = client.get("/api/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item 999 not found"}


def test_create_item_validates_name(client: TestClient) -> None:
    assert client.post("/api/items", json={"name": ""}).status_code == 422
