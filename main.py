import csv
import os
from datetime import datetime

CASES_FILE = "cases.csv"
PARTIES_FILE = "parties.csv"
HEARINGS_FILE = "hearings.csv"

CASE_FIELDS = ["case_number", "case_title", "case_type", "filing_date", "status", "notes"]
PARTY_FIELDS = ["party_id", "case_number", "name", "role"]
HEARING_FIELDS = ["hearing_id", "case_number", "hearing_date", "hearing_time", "courtroom", "notes"]

VALID_STATUSES = ["Open", "Adjourned", "Closed"]


def ensure_csv_file(filename, headers):
    """Create a CSV file with headers if it does not already exist."""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()


def read_records(filename, headers):
    ensure_csv_file(filename, headers)
    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except (OSError, csv.Error) as error:
        print(f"Could not read {filename}: {error}")
        return []


def write_records(filename, headers, records):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(records)
        return True
    except (OSError, csv.Error) as error:
        print(f"Could not save {filename}: {error}")
        return False


def next_id(records, field, prefix):
    numbers = []
    for record in records:
        value = record.get(field, "")
        if value.startswith(prefix):
            try:
                numbers.append(int(value[len(prefix):]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valid_time(value):
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False


def ask_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def show_cases(records):
    if not records:
        print("No cases found.")
        return
    print("\nCASE RECORDS")
    print("-" * 100)
    for case in records:
        print(f"{case['case_number']} | {case['case_title']} | {case['case_type']} | "
              f"{case['filing_date']} | {case['status']}")
    print("-" * 100)


def register_case():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    case_number = next_id(cases, "case_number", "CC")
    title = ask_nonempty("Enter case title: ")
    case_type = ask_nonempty("Enter case type (Civil/Criminal/Family/etc.): ")

    while True:
        filing_date = input("Enter filing date (YYYY-MM-DD): ").strip()
        if valid_date(filing_date):
            break
        print("Invalid date. Example: 2026-11-15")

    notes = input("Brief fictional note (optional): ").strip()
    cases.append({
        "case_number": case_number,
        "case_title": title,
        "case_type": case_type,
        "filing_date": filing_date,
        "status": "Open",
        "notes": notes
    })
    if write_records(CASES_FILE, CASE_FIELDS, cases):
        print(f"Case registered successfully. Case number: {case_number}")


def manage_parties():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    parties = read_records(PARTIES_FILE, PARTY_FIELDS)
    case_number = ask_nonempty("Enter existing case number: ").upper()
    if not any(c["case_number"].upper() == case_number for c in cases):
        print("That case number does not exist. Register the case first.")
        return

    name = ask_nonempty("Enter party's fictional name: ")
    role = ask_nonempty("Enter role (Plaintiff/Defendant/Lawyer/Witness): ")
    party_id = next_id(parties, "party_id", "P")
    parties.append({"party_id": party_id, "case_number": case_number, "name": name, "role": role})
    if write_records(PARTIES_FILE, PARTY_FIELDS, parties):
        print(f"Party saved successfully. Party ID: {party_id}")


def schedule_hearing():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    hearings = read_records(HEARINGS_FILE, HEARING_FIELDS)
    case_number = ask_nonempty("Enter case number for hearing: ").upper()
    if not any(c["case_number"].upper() == case_number for c in cases):
        print("Cannot schedule hearing: case number does not exist.")
        return

    while True:
        hearing_date = input("Enter hearing date (YYYY-MM-DD): ").strip()
        if valid_date(hearing_date):
            break
        print("Invalid date. Example: 2026-11-20")

    while True:
        hearing_time = input("Enter hearing time (HH:MM, 24-hour format): ").strip()
        if valid_time(hearing_time):
            break
        print("Invalid time. Example: 09:30")

    courtroom = ask_nonempty("Enter courtroom: ")
    notes = input("Brief fictional note (optional): ").strip()
    hearing_id = next_id(hearings, "hearing_id", "H")
    hearings.append({
        "hearing_id": hearing_id,
        "case_number": case_number,
        "hearing_date": hearing_date,
        "hearing_time": hearing_time,
        "courtroom": courtroom,
        "notes": notes
    })
    if write_records(HEARINGS_FILE, HEARING_FIELDS, hearings):
        print(f"Hearing scheduled successfully. Hearing ID: {hearing_id}")


def search_case():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    parties = read_records(PARTIES_FILE, PARTY_FIELDS)
    print("\nSearch by: 1. Case number  2. Party name  3. Status")
    choice = input("Choose search type: ").strip()
    term = ask_nonempty("Enter search value: ").lower()

    matches = []
    if choice == "1":
        matches = [c for c in cases if term in c["case_number"].lower()]
    elif choice == "2":
        case_numbers = {p["case_number"] for p in parties if term in p["name"].lower()}
        matches = [c for c in cases if c["case_number"] in case_numbers]
    elif choice == "3":
        matches = [c for c in cases if term == c["status"].lower()]
    else:
        print("Invalid search option.")
        return

    show_cases(matches)
    if choice == "2" and matches:
        print("Matching parties:")
        for party in parties:
            if party["case_number"] in {c["case_number"] for c in matches} and term in party["name"].lower():
                print(f"  {party['name']} ({party['role']}) - {party['case_number']}")


def update_case_status():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    case_number = ask_nonempty("Enter case number to update: ").upper()
    case = next((c for c in cases if c["case_number"].upper() == case_number), None)
    if case is None:
        print("Case not found.")
        return

    print("Available statuses:", ", ".join(VALID_STATUSES))
    status = ask_nonempty("Enter new status: ").title()
    if status not in VALID_STATUSES:
        print("Invalid status. Status was not changed.")
        return
    case["status"] = status
    if write_records(CASES_FILE, CASE_FIELDS, cases):
        print(f"{case_number} status updated to {status}.")


def view_hearings_by_date():
    hearings = read_records(HEARINGS_FILE, HEARING_FIELDS)
    while True:
        selected_date = input("Enter hearing date (YYYY-MM-DD): ").strip()
        if valid_date(selected_date):
            break
        print("Invalid date. Use YYYY-MM-DD.")
    matches = [h for h in hearings if h["hearing_date"] == selected_date]
    if not matches:
        print("No hearings scheduled for that date.")
        return
    print("\nHEARINGS")
    for h in sorted(matches, key=lambda item: item["hearing_time"]):
        print(f"{h['hearing_id']} | Case: {h['case_number']} | {h['hearing_time']} | "
              f"{h['courtroom']} | {h['notes']}")


def basic_reports():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    hearings = read_records(HEARINGS_FILE, HEARING_FIELDS)
    print("\nBASIC REPORTS")
    print(f"Total registered cases: {len(cases)}")
    open_cases = [c for c in cases if c["status"].lower() == "open"]
    print(f"Open cases: {len(open_cases)}")
    show_cases(open_cases)
    print(f"Total scheduled hearings: {len(hearings)}")


def list_all_records():
    cases = read_records(CASES_FILE, CASE_FIELDS)
    parties = read_records(PARTIES_FILE, PARTY_FIELDS)
    hearings = read_records(HEARINGS_FILE, HEARING_FIELDS)
    print("\n1. Cases  2. Parties  3. Hearings")
    choice = input("Choose records to display: ").strip()
    if choice == "1":
        show_cases(cases)
    elif choice == "2":
        for p in parties:
            print(f"{p['party_id']} | {p['case_number']} | {p['name']} | {p['role']}")
        if not parties:
            print("No party records found.")
    elif choice == "3":
        for h in hearings:
            print(f"{h['hearing_id']} | {h['case_number']} | {h['hearing_date']} | "
                  f"{h['hearing_time']} | {h['courtroom']}")
        if not hearings:
            print("No hearing records found.")
    else:
        print("Invalid option.")


def delete_case():
    """Delete a case only when it has no linked parties or hearings."""
    cases = read_records(CASES_FILE, CASE_FIELDS)
    parties = read_records(PARTIES_FILE, PARTY_FIELDS)
    hearings = read_records(HEARINGS_FILE, HEARING_FIELDS)
    case_number = ask_nonempty("Enter case number to delete: ").upper()
    if not any(c["case_number"].upper() == case_number for c in cases):
        print("Case not found.")
        return
    if any(p["case_number"].upper() == case_number for p in parties) or \
       any(h["case_number"].upper() == case_number for h in hearings):
        print("This case has linked party/hearing records and cannot be deleted.")
        return
    confirm = input("Type YES to confirm deletion: ").strip()
    if confirm == "YES":
        cases = [c for c in cases if c["case_number"].upper() != case_number]
        if write_records(CASES_FILE, CASE_FIELDS, cases):
            print("Case deleted.")
    else:
        print("Deletion cancelled.")


def initialize_files():
    ensure_csv_file(CASES_FILE, CASE_FIELDS)
    ensure_csv_file(PARTIES_FILE, PARTY_FIELDS)
    ensure_csv_file(HEARINGS_FILE, HEARING_FIELDS)


def main():
    initialize_files()
    while True:
        print("\n===== COURT CASE MANAGEMENT SYSTEM =====")
        print("1. Register Case")
        print("2. Manage Parties")
        print("3. Schedule Hearing")
        print("4. Search Case")
        print("5. Update Case Status")
        print("6. View Hearings by Date")
        print("7. Basic Reports")
        print("8. Display All Records")
        print("9. Delete Case")
        print("10. Exit")
        choice = input("Select an option (1-10): ").strip()

        actions = {
            "1": register_case,
            "2": manage_parties,
            "3": schedule_hearing,
            "4": search_case,
            "5": update_case_status,
            "6": view_hearings_by_date,
            "7": basic_reports,
            "8": list_all_records,
            "9": delete_case
        }
        if choice == "10":
            print("Thank you for using the Court Case Management System.")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled.")
            except Exception as error:
                print(f"An unexpected error occurred: {error}")
        else:
            print("Invalid menu option. Please choose a number from 1 to 10.")


if __name__ == "__main__":
    main()
