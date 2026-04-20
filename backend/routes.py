from flask import Blueprint, request, jsonify
from models import sessions, DEPT_SESSION_LIMITS, DEPT_PROGRAMS, participant_session_map, participants

api = Blueprint("api", __name__)

SEED_PARTICIPANTS = (
    [(f"PA{i:03d}", f"Division A Participant {i}", "Division A") for i in range(1, 25)] +
    [(f"PB{i:03d}", f"Division B Participant {i}", "Division B") for i in range(1, 19)] +
    [(f"PC{i:03d}", f"Division C Participant {i}", "Division C") for i in range(1, 19)]
)


@api.route("/seed", methods=["POST"])
def seed():
    for pid, name, dept in SEED_PARTICIPANTS:
        if pid not in participants:
            participants[pid] = {"name": name, "department": dept}
    return jsonify({"message": f"Seeded {len(participants)} participants"}), 201


def bad_request(msg):
    return jsonify({"error": msg}), 400


# ── Participants ──────────────────────────────────────────────────────────────

@api.route("/participants", methods=["POST"])
def register_participant():
    """
    Register a new participant.
    ---
    tags: [Participants]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required: [id, name, department]
          properties:
            id:         {type: string, example: P001}
            name:       {type: string, example: Jane Doe}
            department: {type: string, example: Division A}
    responses:
      201:
        description: Participant registered
      400:
        description: Missing or invalid fields
      409:
        description: Participant already registered
    """
    data = request.get_json(silent=True)
    if not data:
        return bad_request("Request body must be valid JSON")

    pid  = data.get("id")
    name = data.get("name")
    dept = data.get("department")

    if not all([pid, name, dept]):
        return bad_request("id, name and department are required")
    if not all(isinstance(v, str) for v in [pid, name, dept]):
        return bad_request("id, name and department must be strings")
    if dept not in DEPT_SESSION_LIMITS:
        return bad_request(f"Invalid department. Valid options: {list(DEPT_SESSION_LIMITS)}")
    if pid in participants:
        return jsonify({"error": "Participant already registered"}), 409

    participants[pid] = {"name": name, "department": dept, "program": DEPT_PROGRAMS[dept]}
    return jsonify({"message": "Participant registered", "participant": participants[pid]}), 201


@api.route("/participants", methods=["GET"])
def list_participants():
    """
    List all registered participants.
    ---
    tags: [Participants]
    responses:
      200:
        description: List of participants
    """
    return jsonify([{"id": pid, **info} for pid, info in participants.items()])


# ── Allocations ───────────────────────────────────────────────────────────────

@api.route("/allocate", methods=["POST"])
def allocate():
    """
    Allocate a participant to a session.
    ---
    tags: [Allocations]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required: [participant_id, session_id]
          properties:
            participant_id: {type: string, example: P001}
            session_id:     {type: string, example: morning, enum: [morning, midday, afternoon]}
    responses:
      201:
        description: Allocation successful
      400:
        description: Missing or invalid fields
      404:
        description: Participant or session not found
      409:
        description: Constraint violation
    """
    data = request.get_json(silent=True)
    if not data:
        return bad_request("Request body must be valid JSON")

    pid        = data.get("participant_id")
    session_id = data.get("session_id")

    if not pid or not session_id:
        return jsonify({"valid": False, "error": "participant_id and session_id are required"}), 400
    if not isinstance(pid, str) or not isinstance(session_id, str):
        return jsonify({"valid": False, "error": "participant_id and session_id must be strings"}), 400
    if pid not in participants:
        return jsonify({"valid": False, "error": "Participant not found"}), 404
    if session_id not in sessions:
        return jsonify({"valid": False, "error": f"Session not found. Valid options: {list(sessions)}"}), 404

    session = sessions[session_id]
    dept    = participants[pid]["department"]

    if pid in participant_session_map:
        assigned = participant_session_map[pid]
        return jsonify({"valid": False, "error": f"Participant already assigned to '{assigned}'"}), 409
    if len(session["allocations"]) >= session["capacity"]:
        return jsonify({"valid": False, "error": "Session is fully booked"}), 409

    dept_count = sum(1 for p in session["allocations"] if participants[p]["department"] == dept)
    if dept_count >= DEPT_SESSION_LIMITS[dept]:
        return jsonify({"valid": False, "error": f"Department limit reached for {dept} in this session"}), 409

    session["allocations"].append(pid)
    participant_session_map[pid] = session_id

    return jsonify({
        "valid": True,
        "message": f"{participants[pid]['name']} allocated to {session['name']} session",
        "available_seats": session["capacity"] - len(session["allocations"]),
    }), 201


@api.route("/allocations", methods=["GET"])
def list_allocations():
    """
    View all sessions with available seats.
    ---
    tags: [Allocations]
    responses:
      200:
        description: All sessions with seat availability
    """
    result = {}
    for sid, session in sessions.items():
        result[sid] = {
            "name": session["name"],
            "time_slot": session["time_slot"],
            "capacity": session["capacity"],
            "allocated": len(session["allocations"]),
            "available_seats": session["capacity"] - len(session["allocations"]),
            "participants": [{"id": pid, **participants[pid]} for pid in session["allocations"]],
        }
    return jsonify(result)


@api.route("/allocations/<session_id>", methods=["GET"])
def session_detail(session_id):
    """
    View session detail with department breakdown.
    ---
    tags: [Allocations]
    parameters:
      - in: path
        name: session_id
        required: true
        type: string
        enum: [morning, midday, afternoon]
    responses:
      200:
        description: Session detail
      404:
        description: Session not found
    """
    if session_id not in sessions:
        return jsonify({"error": f"Session not found. Valid options: {list(sessions)}"}), 404

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
                "program": DEPT_PROGRAMS[dept],
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
    """
    Remove a participant from a session.
    ---
    tags: [Allocations]
    parameters:
      - in: path
        name: session_id
        required: true
        type: string
        enum: [morning, midday, afternoon]
      - in: path
        name: participant_id
        required: true
        type: string
    responses:
      200:
        description: Allocation removed
      404:
        description: Session or participant not found
      409:
        description: Participant not allocated to this session
    """
    if session_id not in sessions:
        return jsonify({"error": f"Session not found. Valid options: {list(sessions)}"}), 404
    if participant_id not in participants:
        return jsonify({"error": "Participant not found"}), 404
    if participant_session_map.get(participant_id) != session_id:
        return jsonify({"error": "Participant is not allocated to this session"}), 409

    sessions[session_id]["allocations"].remove(participant_id)
    del participant_session_map[participant_id]
    return jsonify({"message": "Allocation removed successfully"})

