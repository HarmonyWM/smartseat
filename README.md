# SmartSeat - Smart Seat Allocation Platform

A rule-driven seat allocation system that automatically assigns participants to training sessions, eliminating overbooking, duplicate allocations, and department limit violations.

---

## Background

Large organisations managing training programmes at scale often rely on manual tools like spreadsheets, leading to:
- Overbooking of sessions
- Duplicate participant allocations
- No visibility into available capacity
- Unfair distribution across departments

SmartSeat replaces this manual process with an automated, rule-enforcing system that ensures accuracy and fairness.

---

## Problem Statement

Design and build a Smart Seat Allocation Platform that:
- Prevents any training session from being overbooked
- Ensures no participant is assigned more than once
- Respects department seat limits per session
- Provides real-time feedback on available seats and allocation validity

---

## Training Programme Structure

### Sessions

| Session   | Time Slot       | Capacity |
|-----------|-----------------|----------|
| Morning   | 09:00 - 10:30   | 20       |
| Midday    | 11:00 - 12:30   | 20       |
| Afternoon | 13:00 - 14:30   | 20       |

- 3 sessions running on the same day with different time slots
- Each session holds a maximum of **20 participants**
- Total participants: **60**

### Department Seat Allocation

| Department | Total Participants | Max per Session | Total Seats |
|------------|--------------------|-----------------|-------------|
| Division A | 24                 | 8               | 24          |
| Division B | 18                 | 8               | 18          |
| Division C | 18                 | 6               | 18          |
| **Total**  | **60**             | **20**          | **60**      |

The sum of department allocations per session equals 20, matching session capacity.

---

## System Constraints

| # | Constraint                                          | Type            |
|---|-----------------------------------------------------|-----------------|
| 1 | Maximum 20 participants per session                 | Hard Limit      |
| 2 | A participant can only be assigned to one session   | Hard Limit      |
| 3 | Departments cannot exceed their per-session limit   | Hard Limit      |
| 4 | System shows remaining available seats per session  | System Behaviour|

---

## Tech Stack

- **Backend:** Python, Flask
- **Storage:** In-memory (no database required)

---

## Project Structure

```
smartseat/
├── app.py            # Flask entry point
├── models.py         # In-memory data store and constraints
├── routes.py         # All API endpoints
├── requirements.txt  # Dependencies
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd smartseat

# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py
```

The API will be available at `http://127.0.0.1:5000`

---

## API Reference

### Participants

#### Register a Participant
```
POST /api/participants
```
Request body:
```json
{
  "id": "P001",
  "name": "Jane Doe",
  "department": "Division A"
}
```

#### List All Participants
```
GET /api/participants
```

---

### Allocations

#### Allocate a Participant to a Session
```
POST /api/allocate
```
Request body:
```json
{
  "participant_id": "P001",
  "session_id": "morning"
}
```
Valid `session_id` values: `morning`, `midday`, `afternoon`

Success response:
```json
{
  "valid": true,
  "message": "Jane Doe allocated to Morning session",
  "available_seats": 19
}
```

Failed response (example — duplicate allocation):
```json
{
  "valid": false,
  "error": "Participant already assigned to 'morning'"
}
```

#### View All Sessions and Available Seats
```
GET /api/allocations
```

#### View Session Detail with Department Breakdown
```
GET /api/allocations/<session_id>
```
Example: `GET /api/allocations/morning`

#### Remove an Allocation
```
DELETE /api/allocations/<session_id>/<participant_id>
```
Example: `DELETE /api/allocations/morning/P001`

---

## Validation & Feedback

Every allocation request returns a `valid` flag along with either a success message and remaining seat count, or a descriptive error explaining which constraint was violated:

| Scenario                          | Response                                      |
|-----------------------------------|-----------------------------------------------|
| Successful allocation             | `valid: true` + available seats remaining     |
| Session fully booked              | `valid: false` + "Session is fully booked"    |
| Participant already allocated     | `valid: false` + which session they're in     |
| Department limit reached          | `valid: false` + department and session info  |
| Unknown participant or session    | `valid: false` + "not found" message          |
