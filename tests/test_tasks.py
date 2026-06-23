from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token(username: str = "alice", password: str = "secret"):
    r = client.post("/auth/token", data={"username": username, "password": password})
    assert r.status_code == 200
    return r.json()["access_token"]


def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_task_crud_and_dashboard():
    token = get_token()
    headers = auth_headers(token)

    # list empty
    r = client.get("/tasks/", headers=headers)
    assert r.status_code == 200
    assert r.json() == []

    # create
    payload = {"title": "Buy milk", "description": "2 liters"}
    r = client.post("/tasks/", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]

    # get
    r2 = client.get(f"/tasks/{data['id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["title"] == payload["title"]

    # update status
    r3 = client.put(f"/tasks/{data['id']}", json={"status": "in_progress"}, headers=headers)
    assert r3.status_code == 200
    assert r3.json()["status"] == "in_progress"

    # dashboard
    rd = client.get("/tasks/dashboard", headers=headers)
    assert rd.status_code == 200
    assert rd.json()["total"] == 1

    # delete
    r4 = client.delete(f"/tasks/{data['id']}", headers=headers)
    assert r4.status_code == 200
    assert r4.json()["deleted"] is True

    r5 = client.get(f"/tasks/{data['id']}", headers=headers)
    assert r5.status_code == 404
