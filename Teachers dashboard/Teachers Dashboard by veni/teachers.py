import csv
from datetime import date

# ── Shared data ────────────────────────────────────────────
students     = []   # list of {id, name, section}
records      = []   # list of saved attendance records
today_status = {}   # {student_id: status}
today        = str(date.today())

# ── Tiny helpers ───────────────────────────────────────────
def line():
    print("-" * 45)

def pause():
    input("\nPress Enter to continue...")

def pick(prompt, choices):
    """Show a numbered menu and return the chosen option."""
    for i, c in enumerate(choices, 1):
        print(f"  {i}. {c}")
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        print("  Invalid choice, try again.")

# ── Student management ─────────────────────────────────────
def list_students():
    line()
    if not students:
        print("  No students yet.")
    else:
        print(f"  {'ID':<10} {'Name':<20} {'Section'}")
        line()
        for s in students:
            print(f"  {s['id']:<10} {s['name']:<20} {s['section']}")
    line()

def add_student():
    print("\n-- Add Student --")
    sid  = input("  Student ID  : ").strip()
    name = input("  Full Name   : ").strip()
    sec  = input("  Section     : ").strip()
    if not (sid and name and sec):
        print("  All fields are required."); return
    if any(s["id"] == sid for s in students):
        print("  That ID already exists."); return
    students.append({"id": sid, "name": name, "section": sec})
    today_status[sid] = "—"
    print(f"  '{name}' added!")

def delete_student():
    if not students:
        print("  No students to delete."); return
    list_students()
    sid = input("  Enter Student ID to delete: ").strip()
    match = next((s for s in students if s["id"] == sid), None)
    if not match:
        print("  Student not found."); return
    confirm = input(f"  Delete '{match['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        students.remove(match)
        today_status.pop(sid, None)
        print("  Deleted.")

def students_menu():
    options = ["List students", "Add student", "Delete student", "Back"]
    while True:
        print("\n── Students ──────────────────────────")
        choice = pick("  Choose: ", options)
        if   choice == "List students":  list_students()
        elif choice == "Add student":    add_student()
        elif choice == "Delete student": delete_student()
        else: break

# ── Attendance ─────────────────────────────────────────────
STATUSES = ["Present", "Absent", "Late", "Excused"]

def take_attendance():
    if not students:
        print("  No students added yet."); return
    print(f"\n-- Mark Attendance for {today} --")
    print("  (You can re-mark a student anytime before saving)\n")
    for s in students:
        print(f"  Student: {s['name']} (ID: {s['id']})")
        status = pick("  Status: ", STATUSES)
        today_status[s["id"]] = status
        print()
    print("  All students marked!")

def show_today():
    if not students:
        print("  No students."); return
    line()
    print(f"  {'ID':<10} {'Name':<20} {'Status'}")
    line()
    for s in students:
        print(f"  {s['id']:<10} {s['name']:<20} {today_status.get(s['id'], '—')}")
    line()

def save_attendance():
    unmarked = [s["name"] for s in students if today_status.get(s["id"], "—") == "—"]
    if unmarked:
        print(f"  Not yet marked: {', '.join(unmarked)}"); return
    for s in students:
        records.append({
            "date": today, "id": s["id"], "name": s["name"],
            "section": s["section"], "status": today_status[s["id"]]
        })
    print(f"  Attendance for {today} saved! ({len(students)} records)")

def attendance_menu():
    options = ["Mark attendance", "View today's status", "Save attendance", "Back"]
    while True:
        print("\n── Take Attendance ───────────────────")
        choice = pick("  Choose: ", options)
        if   choice == "Mark attendance":     take_attendance()
        elif choice == "View today's status": show_today()
        elif choice == "Save attendance":     save_attendance()
        else: break
        if choice != "Back": pause()

# ── Records ────────────────────────────────────────────────
def view_records():
    if not records:
        print("  No records saved yet."); return
    key = pick("  Sort by: ", ["Date", "Name", "Status"])
    key_map = {"Date": "date", "Name": "name", "Status": "status"}
    sorted_records = sorted(records, key=lambda r: r[key_map[key]])
    line()
    print(f"  {'Date':<12} {'ID':<10} {'Name':<20} {'Section':<10} {'Status'}")
    line()
    for r in sorted_records:
        print(f"  {r['date']:<12} {r['id']:<10} {r['name']:<20} {r['section']:<10} {r['status']}")
    line()

# ── Reports ────────────────────────────────────────────────
def show_summary():
    if not records:
        print("  No data yet. Save attendance first."); return
    total   = len(records)
    present = sum(1 for r in records if r["status"] == "Present")
    absent  = sum(1 for r in records if r["status"] == "Absent")
    late    = sum(1 for r in records if r["status"] == "Late")
    excused = sum(1 for r in records if r["status"] == "Excused")
    rate    = round(present / total * 100, 1)
    line()
    print(f"  Total Records  : {total}")
    print(f"  Present        : {present}")
    print(f"  Absent         : {absent}")
    print(f"  Late           : {late}")
    print(f"  Excused        : {excused}")
    print(f"  Attendance Rate: {rate}%")
    line()

def export_csv():
    if not records:
        print("  No records to export."); return
    fname = f"attendance_{today}.csv"
    with open(fname, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Student ID", "Name", "Section", "Status"])
        for r in records:
            w.writerow([r["date"], r["id"], r["name"], r["section"], r["status"]])
    print(f"  Saved as: {fname}")

def reports_menu():
    options = ["Show summary", "Export to CSV", "Back"]
    while True:
        print("\n── Reports ───────────────────────────")
        choice = pick("  Choose: ", options)
        if   choice == "Show summary":  show_summary()
        elif choice == "Export to CSV": export_csv()
        else: break
        if choice != "Back": pause()

# ── Main ───────────────────────────────────────────────────
def main():
    print("\n  Welcome to Teacher Dashboard!")
    teacher = input("  Enter your name: ").strip() or "Teacher"
    print(f"\n  Hello, {teacher}! Today is {today}.")

    MENU = ["Students", "Take Attendance", "View Records", "Reports", "Exit"]
    while True:
        print("\n══ Main Menu ══════════════════════════")
        choice = pick("  Choose: ", MENU)
        if   choice == "Students":        students_menu()
        elif choice == "Take Attendance": attendance_menu()
        elif choice == "View Records":    view_records(); pause()
        elif choice == "Reports":         reports_menu()
        else:
            print(f"\n  Goodbye, {teacher}!"); break

main()