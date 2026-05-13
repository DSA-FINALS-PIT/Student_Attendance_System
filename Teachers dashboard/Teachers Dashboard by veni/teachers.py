import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import date


# Attendance stored as a list of records
attendanceRecords = []

# Students stored as a list of dicts
students = []

# Today's date
today = str(date.today())

# MAIN WINDOW SETUP
window = tk.Tk()
window.title("Teacher Dashboard")
window.geometry("900x600")
window.config(bg="#f0f4f8")

# TOP BAR SET UP
topBar = tk.Frame(window, bg="#2563eb", height=55)
topBar.pack(fill="x")
topBar.pack_propagate(False)

tk.Label(
    topBar,
    text="  📚 Teacher Dashboard",
    font=("Arial", 16, "bold"),
    bg="#2563eb", fg="white"
).pack(side="left", padx=10, pady=12)


tk.Label(
    topBar,
    text=f"Date: {today}",
    font=("Arial", 11),
    bg="#2563eb", fg="white"
).pack(side="right", padx=20)

# TAB SET UP
# Style the tabs a little
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 11), padding=[12, 6])

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

# Create 4 tab frames
tabStudents   = tk.Frame(tabs, bg="#f0f4f8")
tabAttendance = tk.Frame(tabs, bg="#f0f4f8")
tabRecords    = tk.Frame(tabs, bg="#f0f4f8")
tabReports    = tk.Frame(tabs, bg="#f0f4f8")

tabs.add(tabStudents,   text=" Students")
tabs.add(tabAttendance, text=" Take Attendance")
tabs.add(tabRecords,    text=" View Records")
tabs.add(tabReports,    text=" Reports")


# STYLED BUTTON FUNCTION
def makeButton(parent, text, command, color="#2563eb"):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color, fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=12, pady=6,
        cursor="hand2"
    )


# TAB 1 - STUDENT MANAGEMENT 
tk.Label(tabStudents, text="Student List", font=("Arial", 14, "bold"),
bg="#f0f4f8").pack(anchor="w", padx=15, pady=(12, 4))

# ── Table ──────────────────────────────────────────────────
columns = ("ID", "Name", "Section")
studentTable = ttk.Treeview(tabStudents, columns=columns,
show="headings", height=8)

studentTable.heading("ID",      text="Student ID")
studentTable.heading("Name",    text="Full Name")
studentTable.heading("Section", text="Section")

studentTable.column("ID",      width=100, anchor="center")
studentTable.column("Name",    width=220)
studentTable.column("Section", width=130, anchor="center")

studentTable.pack(padx=15, pady=5, fill="x")

def loadstudentTable():
    # Clear old rows first
    for row in studentTable.get_children():
        studentTable.delete(row)
    # Fill with current students list
    for s in students:
        studentTable.insert("", "end", values=(s["id"], s["name"], s["section"]))

loadstudentTable()

# ── Input form ─────────────────────────────────────────────

formFrame = tk.LabelFrame(tabStudents, text="Add / Edit Student",
font=("Arial", 11), bg="#f0f4f8", padx=10, pady=8)
formFrame.pack(padx=15, pady=8, fill="x")

# Row 1
tk.Label(formFrame, text="Student ID:", bg="#f0f4f8").grid(row=0, column=0, sticky="w", pady=4)
entryId = tk.Entry(formFrame, width=12)
entryId.grid(row=0, column=1, padx=8)

tk.Label(formFrame, text="Full Name:", bg="#f0f4f8").grid(row=0, column=2, sticky="w")
entryName = tk.Entry(formFrame, width=22)
entryName.grid(row=0, column=3, padx=8)

tk.Label(formFrame, text="Section:", bg="#f0f4f8").grid(row=0, column=4, sticky="w")
entrySection = tk.Entry(formFrame, width=14)
entrySection.grid(row=0, column=5, padx=8)

# ── Buttons ────────────────────────────────────────────────

buttonFrame = tk.Frame(tabStudents, bg="#f0f4f8")
buttonFrame.pack(padx=15, anchor="w")

def addStudent():
    sid     = entryId.get().strip()
    name    = entryName.get().strip()
    section = entrySection.get().strip()

    if not sid or not name or not section:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return

    # Check for duplicate ID
    for s in students:
        if s["id"] == sid:
            messagebox.showwarning("Duplicate", "A student with that ID already exists.")
            return

    students.append({"id": sid, "name": name, "section": section})
    loadstudentTable()
    entryId.delete(0, "end")
    entryName.delete(0, "end")
    entrySection.delete(0, "end")
    messagebox.showinfo("Done", f"Student '{name}' added!")

def deleteStudent():
    selected = studentTable.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please click on a student first.")
        return

    values = studentTable.item(selected[0], "values")
    studentId = values[0]
    studentName = values[1]

    confirm = messagebox.askyesno("Delete", f"Delete student '{studentName}'?")
    if confirm:
        # Remove from list
        for i, s in enumerate(students):
            if s["id"] == studentId:
                students.pop(i)
                break
        loadstudentTable()

makeButton(buttonFrame, "➕ Add Student",    addStudent).pack(side="left", padx=4, pady=6)
makeButton(buttonFrame, "🗑 Delete Selected", deleteStudent, color="#dc2626").pack(side="left", padx=4)


# TAKE ATTENDANCE TAB
tk.Label(tabAttendance, text="Mark Today's Attendance",
font=("Arial", 14, "bold"), bg="#f0f4f8").pack(anchor="w", padx=15, pady=(12, 4))

tk.Label(tabAttendance,
text="Select a student, then click a status button below.",
font=("Arial", 10), fg="gray", bg="#f0f4f8").pack(anchor="w", padx=15)

# ── Attendance table ───────────────────────────────────────

attendanceColumn = ("ID", "Name", "Section", "Status")
attendanceTable = ttk.Treeview(tabAttendance, columns=attendanceColumn,
show="headings", height=8)

attendanceTable.heading("ID",      text="Student ID")
attendanceTable.heading("Name",    text="Full Name")
attendanceTable.heading("Section", text="Section")
attendanceTable.heading("Status",  text="Status")

attendanceTable.column("ID",      width=90, anchor="center")
attendanceTable.column("Name",    width=200)
attendanceTable.column("Section", width=120, anchor="center")
attendanceTable.column("Status",  width=100, anchor="center")

attendanceTable.pack(padx=15, pady=8, fill="x")

# Dictionary to track today's attendance  {studentId: status}
todaysStatus = {s["id"]: "—" for s in students}

def loadattendanceTable():
    for row in attendanceTable.get_children():
        attendanceTable.delete(row)
    for s in students:
        status = todaysStatus.get(s["id"], "—")
        attendanceTable.insert("", "end", iid=s["id"],
                        values=(s["id"], s["name"], s["section"], status))

loadattendanceTable()

# ── Status buttons ─────────────────────────────────────────

statusFrame = tk.Frame(tabAttendance, bg="#f0f4f8")
statusFrame.pack(padx=15, anchor="w")

tk.Label(statusFrame, text="Set selected student as:",
        font=("Arial", 10), bg="#f0f4f8").pack(side="left", padx=(0, 8))

def setStatus(status):
    selected = attendanceTable.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please click on a student first.")
        return

    studentId = selected[0]  # We used studentId as iid

    # Update dictionary
    todaysStatus[studentId] = status

    # Refresh table row
    for s in students:
        if s["id"] == studentId:
            attendanceTable.item(studentId, values=(s["id"], s["name"], s["section"], status))
            break

# Four colored buttons for each status
makeButton(statusFrame, "Present", lambda: setStatus("Present"), "#16a34a").pack(side="left", padx=3, pady=6)
makeButton(statusFrame, "Absent",  lambda: setStatus("Absent"),  "#dc2626").pack(side="left", padx=3)
makeButton(statusFrame, "Late",    lambda: setStatus("Late"),    "#d97706").pack(side="left", padx=3)
makeButton(statusFrame, "Excused", lambda: setStatus("Excused"), "#7c3aed").pack(side="left", padx=3)

# ── Save button ────────────────────────────────────────────

def saveAttendance():
    # Check if all students have a status
    unmarked = [sid for sid, status in todaysStatus.items() if status == "—"]
    if unmarked:
        messagebox.showwarning("Incomplete",
            f"{len(unmarked)} student(s) not yet marked.\nPlease mark everyone first.")
        return

    # Save each record
    for s in students:
        attendanceRecords.append({
            "date":    today,
            "id":      s["id"],
            "name":    s["name"],
            "section": s["section"],
            "status":  todaysStatus[s["id"]]
        })

    # Refresh the records tab
    loadrecordTable()

    messagebox.showinfo("Saved", f"Attendance for {today} saved! ✅")

makeButton(tabAttendance, "💾 Save Attendance", saveAttendance, "#2563eb").pack(
    padx=15, pady=6, anchor="w")


# VIEW RECORDS TAB
tk.Label(tabRecords, text="Attendance Records",
        font=("Arial", 14, "bold"), bg="#f0f4f8").pack(anchor="w", padx=15, pady=(12, 4))




recordColumn = ("Date", "ID", "Name", "Section", "Status")
recordTable = ttk.Treeview(tabRecords, columns=recordColumn, show="headings", height=14)

recordTable.heading("Date",    text="Date")
recordTable.heading("ID",      text="Student ID")
recordTable.heading("Name",    text="Full Name")
recordTable.heading("Section", text="Section")
recordTable.heading("Status",  text="Status")

recordTable.column("Date",    width=110, anchor="center")
recordTable.column("ID",      width=90,  anchor="center")
recordTable.column("Name",    width=200)
recordTable.column("Section", width=120, anchor="center")
recordTable.column("Status",  width=100, anchor="center")

recordTable.pack(padx=15, pady=5, fill="both", expand=True)

def sortingbyDate():
    sortedRecords = sorted(attendanceRecords, key=lambda r: r["date"], reverse=True)
    for row in recordTable.get_children():
        recordTable.delete(row)
    for r in sortedRecords:
        recordTable.insert("", "end", values=(
            r["date"], r["id"], r["name"], r["section"], r["status"]
        ))
def sortingbyAZ():
    sortedRecords = sorted(attendanceRecords, key=lambda r: r["name"])
    for row in recordTable.get_children():
        recordTable.delete(row)
    for r in sortedRecords:
        recordTable.insert("", "end", values=(
            r["date"], r["id"], r["name"], r["section"], r["status"]))
def sortingbyStatus():
    sortedRecords = sorted(attendanceRecords, key=lambda r: r["status"])
    for row in recordTable.get_children():
        recordTable.delete(row)
    for r in sortedRecords:
        recordTable.insert("", "end", values=(
            r["date"], r["id"], r["name"], r["section"], r["status"]))
        
def loadrecordTable():
    for row in recordTable.get_children():
        recordTable.delete(row)
    for r in attendanceRecords:
        recordTable.insert("", "end", values=(
            r["date"], r["id"], r["name"], r["section"], r["status"]))

# SORTING BUTTONS
sortFrame = tk.Frame(tabRecords, bg="#f0f4f8")
sortFrame.pack(padx=15, anchor="w")
tk .Label(sortFrame, text="Sort by:", font=("Arial", 10), bg="#f0f4f8").pack(side="left", padx=(0, 8))
makeButton(sortFrame, "Date", sortingbyDate).pack(side="left", padx=3, pady=6)
makeButton(sortFrame, "A-Z", sortingbyAZ).pack(side="left", padx=3)
makeButton(sortFrame, "Status", sortingbyStatus).pack(side="left", padx=3)

# Add scrollbar to records table
recScroll = ttk.Scrollbar(tabRecords, orient="vertical", command=recordTable.yview)
recordTable.configure(yscrollcommand=recScroll.set)


# REPORTS TAB
tk.Label(tabReports, text="Attendance Summary",
        font=("Arial", 14, "bold"), bg="#f0f4f8").pack(anchor="w", padx=15, pady=(12, 4))

# Summary label text
summaryText = tk.StringVar()
summaryText.set("No attendance data yet. Save attendance first.")

tk.Label(tabReports, textvariable=summaryText,
        font=("Arial", 11), bg="#f0f4f8", justify="left").pack(anchor="w", padx=15, pady=8)

def showSummary():
    if not attendanceRecords:
        summaryText.set("No attendance data yet. Save attendance first.")
        return

    total    = len(attendanceRecords)
    present  = sum(1 for r in attendanceRecords if r["status"] == "Present")
    absent   = sum(1 for r in attendanceRecords if r["status"] == "Absent")
    late     = sum(1 for r in attendanceRecords if r["status"] == "Late")
    excused  = sum(1 for r in attendanceRecords if r["status"] == "Excused")

    percentage = round((present / total) * 100, 1) if total > 0 else 0

    summary = (
        f" Total Records   : {total}\n"
        f" Present         : {present}\n"
        f" Absent          : {absent}\n"
        f" Late            : {late}\n"
        f" Excused         : {excused}\n"
        f"\n Attendance Rate : {percentage}%"
    )
    summaryText.set(summary)

def exporttoCSV():
    if not attendanceRecords:
        messagebox.showwarning("No Data", "No attendance records to export yet.")
        return

    # Save file to same folder as this script
    filename = f"attendance_{today}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Student ID", "Name", "Section", "Status"])
        for r in attendanceRecords:
            writer.writerow([r["date"], r["id"], r["name"], r["section"], r["status"]])

    messagebox.showinfo("Exported", f"File saved as:\n{filename}")

# Buttons
reportbuttonFrame = tk.Frame(tabReports, bg="#f0f4f8")
reportbuttonFrame.pack(padx=15, anchor="w")

makeButton(reportbuttonFrame, " Refresh Summary", showSummary).pack(side="left", padx=4, pady=6)
makeButton(reportbuttonFrame, " Export to CSV", exporttoCSV, "#16a34a").pack(side="left", padx=4)


# STATUS BAR
# Hide the main window until the teacher enters their name
window.withdraw()

# This function runs when the teacher clicks Confirm
def confirmsName(event =None):
    name = nameEntry.get().strip()
    if not name:
        messagebox.showwarning("Missing Name", "Please enter your name.", parent=nameDialog)
        return
    nameDialog.destroy()
    # Show the main window now that we have the name
    window.deiconify()
    # Create the status bar with the entered name
    statusBar = tk.Label(window,
        text=f"  Logged in as: {name}  |  {today}",
        font=("Arial", 9), bg="#cbd5e1", anchor="w")
    statusBar.pack(fill="x", side="bottom")

# Small popup window asking for the teacher's name
nameDialog = tk.Toplevel(window)
nameDialog.title("Enter Your Name")
nameDialog.geometry("320x160")
nameDialog.config(bg="#f0f4f8")
nameDialog.resizable(False, False)

# If the teacher closes the dialog without entering a name, close the whole app
nameDialog.protocol("WM_DELETE_WINDOW", window.destroy)

tk.Label(nameDialog, text="Welcome to Teacher Dashboard!",
        font=("Arial", 11, "bold"), bg="#f0f4f8").pack(pady=(20, 4))
tk.Label(nameDialog, text="Please enter your name to continue:",
        font=("Arial", 10), bg="#f0f4f8").pack()

nameEntry = tk.Entry(nameDialog, width=28, font=("Arial", 11))
nameEntry.pack(pady=8)
nameEntry.focus()

# Allow pressing Enter to confirm
nameDialog.bind("<Return>", confirmsName)

tk.Button(nameDialog, text="Confirm", command=confirmsName,
        bg="#2563eb", fg="white", font=("Arial", 10, "bold"),
        relief="flat", padx=16, pady=6, cursor="hand2").pack()


# RUN MAIN WINDOW APP

window.mainloop()