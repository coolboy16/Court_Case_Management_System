# Court Case Management System

## Project overview
A beginner-friendly Python 3 console application for recording fictional court cases, parties, hearing schedules, and case statuses. It is an educational demonstration only, not a legal advice system or an official court-record system.

## Features
- Register cases with automatically generated case numbers.
- Add parties to an existing case.
- Schedule hearings only for existing cases.
- Search cases by case number, party name, or status.
- Update a case status to Open, Adjourned, or Closed.
- View hearings for a selected date.
- View basic reports, including open cases.
- Display all cases, parties, or hearings.
- Delete a case only if it has no linked party or hearing records.
- Save information in CSV files so it remains after restarting.

## Requirements
- Python 3.8 or newer
- No third-party packages are required.

## How to run
1. Extract the ZIP folder.
2. Open the extracted `Court_Case_Management_System` folder in VS Code.
3. Open the VS Code terminal.
4. Run:

   ```bash
   python main.py
   ```

   On some systems, use `python3 main.py`.

5. Select a numbered menu option. Choose `10` to exit.

The program creates `cases.csv`, `parties.csv`, and `hearings.csv` with headers automatically if they are missing or empty.

## CSV files
- `cases.csv`: case number, title, type, filing date, status, notes.
- `parties.csv`: party ID, linked case number, name, role.
- `hearings.csv`: hearing ID, linked case number, date, time, courtroom, notes.

The included CSV files contain 30 fictional case records and related fictional demonstration records. You may add more records through the menu.

## Run the tests
From the project folder, run:

```bash
python -m unittest -v
```

The tests check case searching, rejection of a hearing for a non-existing case, case status updates, and date/time validation.

## Demonstration guide
1. Start the program with `python main.py`.
2. Choose `1` and register a fictional case. Use a date such as `2026-11-12`.
3. Choose `2` and add a fictional plaintiff or defendant to the new case number.
4. Choose `3` and schedule a hearing for that case, using a date such as `2026-11-20` and time `09:30`.
5. Choose `4` to search by the case number or party name.
6. Choose `5` to change the case status to `Adjourned` or `Closed`.
7. Choose `6` to view hearings for `2026-11-20`.
8. Choose `7` to show the basic report.
9. Exit with `10`, start the program again, and show that the records are still saved in the CSV files.

## Test checklist
- [ ] Register a valid case and confirm it appears in the case list.
- [ ] Try a blank case title and confirm the program asks again.
- [ ] Enter a date in the wrong format and confirm it is rejected.
- [ ] Search for an existing case number.
- [ ] Search for a non-existing case number.
- [ ] Search by a fictional party name and by status.
- [ ] Schedule a hearing for an existing case.
- [ ] Try scheduling a hearing for a non-existing case number.
- [ ] Update a case to `Closed`.
- [ ] Try an invalid status and confirm it is not saved.
- [ ] Restart the program and confirm saved records remain.
- [ ] Try deleting a case with linked records and confirm deletion is blocked.

## Limitations and safe-use rules
- Use fictional names and fictional case details only.
- Do not enter confidential, sensitive, or real court information.
- This project does not provide legal advice and does not replace official court records.
- It does not include user accounts, security controls, document management, network access, or automatic courtroom conflict detection.
- CSV files are suitable for a small classroom project, not a production court system.
