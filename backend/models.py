sessions = {
    "morning": {"name": "Morning", "time_slot": "09:00 - 10:30", "capacity": 20, "allocations": []},
    "midday":  {"name": "Midday",  "time_slot": "11:00 - 12:30", "capacity": 20, "allocations": []},
    "afternoon":{"name": "Afternoon","time_slot": "13:00 - 14:30","capacity": 20, "allocations": []},
}

# Max seats per department per session
DEPT_SESSION_LIMITS = {
    "Division A": 8,
    "Division B": 8,
    "Division C": 6,
}

# participant_id -> session_id  (enforces one session per participant)
participant_session_map = {}

# participants registry: id -> {name, department}
participants = {}
