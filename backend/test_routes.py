import pytest
from app import app
import models


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory state before each test."""
    models.participants.clear()
    models.participant_session_map.clear()
    for s in models.sessions.values():
        s["allocations"].clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def register(client, pid, name, dept):
    return client.post("/api/participants", json={"id": pid, "name": name, "department": dept})


def allocate(client, pid, session_id):
    return client.post("/api/allocate", json={"participant_id": pid, "session_id": session_id})


# ── Participants ──────────────────────────────────────────────────────────────

def test_register_participant(client):
    res = register(client, "P001", "Jane Doe", "Division A")
    assert res.status_code == 201
    assert res.get_json()["message"] == "Participant registered"


def test_register_duplicate(client):
    register(client, "P001", "Jane Doe", "Division A")
    res = register(client, "P001", "Jane Doe", "Division A")
    assert res.status_code == 409


def test_register_invalid_department(client):
    res = register(client, "P001", "Jane Doe", "Division Z")
    assert res.status_code == 400


def test_list_participants(client):
    register(client, "P001", "Jane Doe", "Division A")
    res = client.get("/api/participants")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


# ── Allocations ───────────────────────────────────────────────────────────────

def test_allocate_success(client):
    register(client, "P001", "Jane Doe", "Division A")
    res = allocate(client, "P001", "morning")
    data = res.get_json()
    assert res.status_code == 201
    assert data["valid"] is True
    assert data["available_seats"] == 19


def test_allocate_unknown_participant(client):
    res = allocate(client, "P999", "morning")
    assert res.status_code == 404
    assert res.get_json()["valid"] is False


def test_allocate_unknown_session(client):
    register(client, "P001", "Jane Doe", "Division A")
    res = allocate(client, "P001", "evening")
    assert res.status_code == 404
    assert res.get_json()["valid"] is False


def test_duplicate_allocation(client):
    register(client, "P001", "Jane Doe", "Division A")
    allocate(client, "P001", "morning")
    res = allocate(client, "P001", "midday")
    assert res.status_code == 409
    assert "already assigned" in res.get_json()["error"]


def test_session_fully_booked(client):
    for i in range(21):
        dept = "Division A" if i < 8 else ("Division B" if i < 16 else "Division C")
        register(client, f"P{i:03}", f"Person {i}", dept)

    for i in range(20):
        allocate(client, f"P{i:03}", "morning")

    res = allocate(client, "P020", "morning")
    assert res.status_code == 409
    assert "fully booked" in res.get_json()["error"]


def test_department_limit_reached(client):
    # Fill Division A's limit (8) in morning
    for i in range(9):
        register(client, f"PA{i:03}", f"Person {i}", "Division A")
    for i in range(8):
        allocate(client, f"PA{i:03}", "morning")

    res = allocate(client, "PA008", "morning")
    assert res.status_code == 409
    assert "Department limit reached" in res.get_json()["error"]


# ── Session Views ─────────────────────────────────────────────────────────────

def test_list_allocations(client):
    res = client.get("/api/allocations")
    assert res.status_code == 200
    data = res.get_json()
    assert "morning" in data
    assert data["morning"]["available_seats"] == 20


def test_session_detail(client):
    res = client.get("/api/allocations/morning")
    assert res.status_code == 200
    assert res.get_json()["session_id"] == "morning"


def test_session_detail_not_found(client):
    res = client.get("/api/allocations/evening")
    assert res.status_code == 404


# ── Remove Allocation ─────────────────────────────────────────────────────────

def test_remove_allocation(client):
    register(client, "P001", "Jane Doe", "Division A")
    allocate(client, "P001", "morning")
    res = client.delete("/api/allocations/morning/P001")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Allocation removed successfully"


def test_remove_allocation_not_assigned(client):
    register(client, "P001", "Jane Doe", "Division A")
    res = client.delete("/api/allocations/morning/P001")
    assert res.status_code == 409
