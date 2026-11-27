import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    main.reset_store()
    with TestClient(main.app) as test_client:
        yield test_client
    main.reset_store()


def test_create_and_retrieve_task_defaults(client):
    res = client.post("/tasks", json={"title": "Study FastAPI"})
    assert res.status_code == 201
    created = res.json()
    assert created == {
        "id": 1,
        "title": "Study FastAPI",
        "description": "",
        "completed": False,
    }

    get_res = client.get("/tasks/1")
    assert get_res.status_code == 200
    assert get_res.json() == created


def test_filter_completed_and_incomplete_tasks(client):
    client.post("/tasks", json={"title": "Incomplete task", "completed": False})
    client.post("/tasks", json={"title": "Completed task", "completed": True})

    all_res = client.get("/tasks")
    assert all_res.status_code == 200
    assert len(all_res.json()) == 2

    completed_res = client.get("/tasks", params={"completed": True})
    assert completed_res.status_code == 200
    assert [t["title"] for t in completed_res.json()] == ["Completed task"]

    incomplete_res = client.get("/tasks", params={"completed": False})
    assert incomplete_res.status_code == 200
    assert [t["title"] for t in incomplete_res.json()] == ["Incomplete task"]

    # Delete completed task so filter returns empty list with 200
    client.delete("/tasks/2")
    empty_filter = client.get("/tasks", params={"completed": True})
    assert empty_filter.status_code == 200
    assert empty_filter.json() == []


def test_reject_invalid_titles_without_mutating_store(client):
    for bad_payload in [
        {},  # missing title
        {"title": ""},  # empty title
        {"title": "a" * 121},  # > 120 chars
    ]:
        res = client.post("/tasks", json=bad_payload)
        assert res.status_code == 422

    assert client.get("/tasks").json() == []
    # Next valid creation must still get ID 1
    valid = client.post("/tasks", json={"title": "First valid"})
    assert valid.json()["id"] == 1


def test_missing_and_invalid_path_ids(client):
    assert client.get("/tasks/999").status_code == 404
    assert client.get("/tasks/abc").status_code == 422
    assert client.get("/tasks/0").status_code == 422


def test_replace_task_and_reject_incomplete_put(client):
    client.post("/tasks", json={"title": "Initial", "description": "Old", "completed": False})

    # Incomplete PUT (missing 'completed') must return 422 and leave task unchanged
    bad_put = client.put("/tasks/1", json={"title": "Partial", "description": "New"})
    assert bad_put.status_code == 422
    assert client.get("/tasks/1").json() == {
        "id": 1,
        "title": "Initial",
        "description": "Old",
        "completed": False,
    }

    # Complete PUT replaces editable fields while preserving ID 1
    good_put = client.put(
        "/tasks/1",
        json={"title": "Updated", "description": "Done", "completed": True},
    )
    assert good_put.status_code == 200
    assert good_put.json() == {
        "id": 1,
        "title": "Updated",
        "description": "Done",
        "completed": True,
    }


def test_delete_task_returns_204_and_subsequent_calls_return_404(client):
    client.post("/tasks", json={"title": "Temp task"})

    del_res = client.delete("/tasks/1")
    assert del_res.status_code == 204
    assert del_res.content == b""

    assert client.get("/tasks/1").status_code == 404
    assert client.delete("/tasks/1").status_code == 404


def test_delete_does_not_reuse_ids_or_overwrite_existing(client):
    t1 = client.post("/tasks", json={"title": "Task 1"}).json()
    t2 = client.post("/tasks", json={"title": "Task 2"}).json()
    assert t1["id"] == 1 and t2["id"] == 2

    client.delete("/tasks/1")

    t3 = client.post("/tasks", json={"title": "Task 3"}).json()
    assert t3["id"] == 3
    remaining = client.get("/tasks").json()
    assert [t["id"] for t in remaining] == [2, 3]
