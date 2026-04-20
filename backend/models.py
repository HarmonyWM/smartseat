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

# Training program assigned to each department
DEPT_PROGRAMS = {
    "Division A": "Leadership Development",
    "Division B": "Technical Skills",
    "Division C": "Customer Service",
}

# participant_id -> session_id  (enforces one session per participant)
participant_session_map = {}

# participants registry: id -> {name, department}
participants = {
    # Division A - 24 participants
    "PA001": {"name": "Lebo Mokoena",     "department": "Division A"},
    "PA002": {"name": "Sipho Dlamini",    "department": "Division A"},
    "PA003": {"name": "Jane Doe",         "department": "Division A"},
    "PA004": {"name": "Thabo Nkosi",      "department": "Division A"},
    "PA005": {"name": "Naledi Khumalo",   "department": "Division A"},
    "PA006": {"name": "Kagiso Sithole",   "department": "Division A"},
    "PA007": {"name": "Zanele Mthembu",   "department": "Division A"},
    "PA008": {"name": "Bongani Zulu",     "department": "Division A"},
    "PA009": {"name": "Mpho Molefe",      "department": "Division A"},
    "PA010": {"name": "Tebogo Mahlangu",  "department": "Division A"},
    "PA011": {"name": "Lerato Ndlovu",    "department": "Division A"},
    "PA012": {"name": "Siyanda Cele",     "department": "Division A"},
    "PA013": {"name": "Ayanda Mkhize",    "department": "Division A"},
    "PA014": {"name": "Nompumelelo Dube", "department": "Division A"},
    "PA015": {"name": "Lungelo Shabalala","department": "Division A"},
    "PA016": {"name": "Precious Motha",   "department": "Division A"},
    "PA017": {"name": "Sibusiso Ntuli",   "department": "Division A"},
    "PA018": {"name": "Nomsa Vilakazi",   "department": "Division A"},
    "PA019": {"name": "Mandla Buthelezi", "department": "Division A"},
    "PA020": {"name": "Lindiwe Mthethwa", "department": "Division A"},
    "PA021": {"name": "Sandile Majola",   "department": "Division A"},
    "PA022": {"name": "Nokwanda Gumede",  "department": "Division A"},
    "PA023": {"name": "Musa Hadebe",      "department": "Division A"},
    "PA024": {"name": "Thandeka Ngcobo",  "department": "Division A"},
    # Division B - 18 participants
    "PB001": {"name": "John Smith",       "department": "Division B"},
    "PB002": {"name": "Aisha Patel",      "department": "Division B"},
    "PB003": {"name": "Mike Peters",      "department": "Division B"},
    "PB004": {"name": "Sarah Johnson",    "department": "Division B"},
    "PB005": {"name": "David Nkosi",      "department": "Division B"},
    "PB006": {"name": "Fatima Osman",     "department": "Division B"},
    "PB007": {"name": "James Mokoena",    "department": "Division B"},
    "PB008": {"name": "Priya Singh",      "department": "Division B"},
    "PB009": {"name": "Carlos Ferreira",  "department": "Division B"},
    "PB010": {"name": "Amara Diallo",     "department": "Division B"},
    "PB011": {"name": "Ruan van Wyk",     "department": "Division B"},
    "PB012": {"name": "Yusuf Adams",      "department": "Division B"},
    "PB013": {"name": "Chidi Okafor",     "department": "Division B"},
    "PB014": {"name": "Mei Lin",          "department": "Division B"},
    "PB015": {"name": "Tariq Hassan",     "department": "Division B"},
    "PB016": {"name": "Elena Petrov",     "department": "Division B"},
    "PB017": {"name": "Omar Shaikh",      "department": "Division B"},
    "PB018": {"name": "Nina Botha",       "department": "Division B"},
    # Division C - 18 participants
    "PC001": {"name": "Zanele Dlamini",   "department": "Division C"},
    "PC002": {"name": "Rohan Naidoo",     "department": "Division C"},
    "PC003": {"name": "Liesl du Plessis", "department": "Division C"},
    "PC004": {"name": "Kwame Mensah",     "department": "Division C"},
    "PC005": {"name": "Ingrid Visser",    "department": "Division C"},
    "PC006": {"name": "Tolu Adeyemi",     "department": "Division C"},
    "PC007": {"name": "Brendan Jacobs",   "department": "Division C"},
    "PC008": {"name": "Sana Malik",       "department": "Division C"},
    "PC009": {"name": "Kofi Asante",      "department": "Division C"},
    "PC010": {"name": "Miriam Fourie",    "department": "Division C"},
    "PC011": {"name": "Deon Swanepoel",   "department": "Division C"},
    "PC012": {"name": "Nia Mensah",       "department": "Division C"},
    "PC013": {"name": "Arjun Reddy",      "department": "Division C"},
    "PC014": {"name": "Claudia Ferreira", "department": "Division C"},
    "PC015": {"name": "Siphamandla Zulu", "department": "Division C"},
    "PC016": {"name": "Hana Kimura",      "department": "Division C"},
    "PC017": {"name": "Emeka Eze",        "department": "Division C"},
    "PC018": {"name": "Bianca Lombard",   "department": "Division C"},
}
