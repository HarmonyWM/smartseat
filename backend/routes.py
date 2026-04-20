from flask import Blueprint, request, jsonify
from models import sessions, DEPT_SESSION_LIMITS, participant_session_map, participants

api = Blueprint("api", __name__)


# ── Participants ──────────────────────────────────────────────────────────────

@api.route("/participants", methods=["POST"])
def register_participant():
    data = request.get_json()
    pid  = data.get("id")
    name = data.get("name")
    dept = data.get("department")

    if not all([pid, name, dept]):
        return jsonify({"error": "id, name and department are required"}), 400
    if dept not in DEPT_SESSION_LIMITS:
        return jsonify({"error": f"Unknown department. Valid: {list(DEPT_SESSION_LIMITS)}"}), 400
    if pid in participants:
        return jsonify({"error": "Participant already registered"}), 409

    participants[pid] = {"name": name, "department": dept}
    return jsonify({"message": "Participant registered", "participant": participants[pid]}), 201


@api.route("/participants", methods=["GET"])
def list_participants():
    return jsonify([{"id": pid, **info} for pid, info in participants.items()])


# ── Allocations ───────────────────────────────────────────────────────────────

@api.route("/allocate", methods=["POST"])
def allocate():
    data       = request.get_json()
    pid        = data.get("participant_id")
    session_id = data.get("session_id")

    # Validate inputs
    if pid not in participants:
        return jsonify({"valid": False, "error": "Participant not found"}), 404
    if session_id not in sessions:
        return jsonify({"valid": False, "error": "Session not found"}), 404

    session = sessions[session_id]
    dept    = participants[pid]["department"]

    # Constraint 2: one session per participant
    if pid in participant_session_map:
        assigned = participant_session_map[pid]
        return jsonify({"valid": False, "error": f"Participant already assigned to '{assigned}'"}), 409

    # Constraint 1: session capacity
    if len(session["allocations"]) >= session["capacity"]:
        return jsonify({"valid": False, "error": "Session is fully booked"}), 409

    # Constraint 3: department limit per session
    dept_count = sum(1 for p in session["allocations"] if participants[p]["department"] == dept)
    if dept_count >= DEPT_SESSION_LIMITS[dept]:
        return jsonify({"valid": False, "error": f"Department limit reached for {dept} in this session"}), 409

    # All checks passed — allocate
    session["allocations"].append(pid)
    participant_session_map[pid] = session_id

    return jsonify({
        "valid": True,
        "message": f"{participants[pid]['name']} allocated to {session['name']} session",
        "available_seats": session["capacity"] - len(session["allocations"]),
    }), 201


@api.route("/allocations", methods=["GET"])
def list_allocations():
    result = {}
    for sid, session in sessions.items():
        result[sid] = {
            "name": session["name"],
            "time_slot": session["time_slot"],
            "capacity": session["capacity"],
            "allocated": len(session["allocations"]),
            "available_seats": session["capacity"] - len(session["allocations"]),
            "participants": [
                {"id": pid, **participants[pid]} for pid in session["allocations"]
            ],
        }
    return jsonify(result)


@api.route("/allocations/<session_id>", methods=["GET"])
def session_detail(session_id):
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404

    session = sessions[session_id]
    dept_breakdown = {}
    for pid in session["allocations"]:
        dept = participants[pid]["department"]
        dept_breakdown[dept] = dept_breakdown.get(dept, 0) + 1

    return jsonify({
        "session_id": session_id,
        "name": session["name"],
        "time_slot": session["time_slot"],
        "capacity": session["capacity"],
        "allocated": len(session["allocations"]),
        "available_seats": session["capacity"] - len(session["allocations"]),
        "department_breakdown": {
            dept: {
                "allocated": dept_breakdown.get(dept, 0),
                "limit": DEPT_SESSION_LIMITS[dept],
                "remaining": DEPT_SESSION_LIMITS[dept] - dept_breakdown.get(dept, 0),
            }
            for dept in DEPT_SESSION_LIMITS
        },
        "participants": [{"id": pid, **participants[pid]} for pid in session["allocations"]],
    })


@api.route("/allocations/<session_id>/<participant_id>", methods=["DELETE"])
def remove_allocation(session_id, participant_id):
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    if participant_id not in participants:
        return jsonify({"error": "Participant not found"}), 404
    if participant_session_map.get(participant_id) != session_id:
        return jsonify({"error": "Participant is not allocated to this session"}), 409

    sessions[session_id]["allocations"].remove(participant_id)
    del participant_session_map[participant_id]
    return jsonify({"message": "Allocation removed successfully"})
