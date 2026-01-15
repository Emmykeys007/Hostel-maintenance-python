from __future__ import annotations
import csv
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "requests.csv")


# -----------------------------
# Domain Model
# -----------------------------
STATUSES = ["Submitted", "InProgress", "Resolved", "Closed"]

ALLOWED_TRANSITIONS = {
    "Submitted": ["InProgress"],
    "InProgress": ["Resolved"],
    "Resolved": ["Closed"],
    "Closed": []
}


@dataclass
class Request:
    id: int
    student_name: str
    matric: str
    hostel: str
    room: str
    category: str
    description: str
    status: str
    created_at: str


# -----------------------------
# Storage Layer (CSV)
# -----------------------------
FIELDNAMES = [
    "id",
    "student_name",
    "matric",
    "hostel",
    "room",
    "category",
    "description",
    "status",
    "created_at",
]


def ensure_storage() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_requests() -> List[Request]:
    ensure_storage()
    requests: List[Request] = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                requests.append(
                    Request(
                        id=int(row["id"]),
                        student_name=row["student_name"],
                        matric=row["matric"],
                        hostel=row["hostel"],
                        room=row["room"],
                        category=row["category"],
                        description=row["description"],
                        status=row["status"],
                        created_at=row["created_at"],
                    )
                )
            except Exception:
                # Skip corrupt lines safely
                continue
    return requests


def save_requests(requests: List[Request]) -> None:
    ensure_storage()
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in requests:
            writer.writerow(asdict(r))


def next_id(requests: List[Request]) -> int:
    return (max((r.id for r in requests), default=0) + 1)


# -----------------------------
# Helpers
# -----------------------------
def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def input_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")


def input_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Invalid number. Try again.")


def can_transition(current: str, new: str) -> bool:
    return new in ALLOWED_TRANSITIONS.get(current, [])


def print_request(r: Request) -> None:
    print(
        f"ID: {r.id} | Matric: {r.matric} | Name: {r.student_name} | "
        f"Hostel: {r.hostel} | Room: {r.room} | Category: {r.category} | "
        f"Status: {r.status} | Created: {r.created_at}"
    )
    print(f"  Description: {r.description}")
    print("-" * 80)


# -----------------------------
# Menus
# -----------------------------
def student_menu(requests: List[Request]) -> List[Request]:
    print("\n--- STUDENT ---")
    name = input_non_empty("Enter your full name: ")
    matric = input_non_empty("Enter your matric number: ")

    while True:
        print("\n--- STUDENT MENU ---")
        print("1. Create maintenance request")
        print("2. View my requests")
        print("0. Back")

        choice = input_int("Choose: ")
        if choice == 0:
            return requests

        if choice == 1:
            hostel = input_non_empty("Hostel name: ")
            room = input_non_empty("Room number: ")
            category = input_non_empty("Category (Electricity/Plumbing/Carpentry/Other): ")
            description = input_non_empty("Describe the issue: ")

            new_req = Request(
                id=next_id(requests),
                student_name=name,
                matric=matric,
                hostel=hostel,
                room=room,
                category=category,
                description=description,
                status="Submitted",
                created_at=now_ts(),
            )
            requests.append(new_req)
            save_requests(requests)

            print(f"\n✅ Request submitted successfully! Your Request ID is {new_req.id}")

        elif choice == 2:
            print("\n--- MY REQUESTS ---")
            mine = [r for r in requests if r.matric == matric]
            if not mine:
                print("No requests found for this matric number.")
            else:
                for r in mine:
                    print_request(r)
        else:
            print("Invalid choice.")
    # unreachable


def admin_login() -> bool:
    # Demo login. In a real system, store hashed credentials.
    ADMIN_USER = "admin"
    ADMIN_PASS = "1234"

    print("\n--- ADMIN LOGIN ---")
    u = input_non_empty("Username: ")
    p = input_non_empty("Password: ")
    return u == ADMIN_USER and p == ADMIN_PASS


def admin_menu(requests: List[Request]) -> List[Request]:
    if not admin_login():
        print("❌ Login failed.")
        return requests

    while True:
        print("\n--- ADMIN MENU ---")
        print("1. View all requests")
        print("2. Update request status")
        print("0. Back")

        choice = input_int("Choose: ")
        if choice == 0:
            return requests

        if choice == 1:
            print("\n--- ALL REQUESTS ---")
            if not requests:
                print("No requests yet.")
            else:
                for r in requests:
                    print_request(r)

        elif choice == 2:
            req_id = input_int("Enter Request ID to update: ")

            req: Optional[Request] = next((r for r in requests if r.id == req_id), None)
            if not req:
                print("Request not found.")
                continue

            print(f"Current status: {req.status}")
            print("New Status Options:")
            print("1. InProgress")
            print("2. Resolved")
            print("3. Closed")

            sel = input_int("Select: ")
            if sel == 1:
                new_status = "InProgress"
            elif sel == 2:
                new_status = "Resolved"
            elif sel == 3:
                new_status = "Closed"
            else:
                print("Invalid selection.")
                continue

            if not can_transition(req.status, new_status):
                print(f"❌ Invalid transition: {req.status} -> {new_status}")
                continue

            req.status = new_status
            save_requests(requests)
            print("✅ Status updated successfully.")

        else:
            print("Invalid choice.")
    # unreachable


def main() -> None:
    print("=== HOSTEL MAINTENANCE REQUEST SYSTEM (PYTHON) ===")
    requests = load_requests()

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Student")
        print("2. Admin")
        print("0. Exit")

        choice = input_int("Choose: ")
        if choice == 0:
            print("Goodbye!")
            break

        # Reload before each major action (keeps file as source of truth)
        requests = load_requests()

        if choice == 1:
            requests = student_menu(requests)
        elif choice == 2:
            requests = admin_menu(requests)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()