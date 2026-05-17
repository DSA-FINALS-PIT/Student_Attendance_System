import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import date

# =========================================================
# TEACHER DASHBOARD
# =========================================================

def open_dashboard(username, logout_callback):

    # Empty data structures to hold students and attendance records
    students     = []   # list of {id, name, section}
    records      = []   # list of saved attendance records
    today_status = {}   # {student_id: status}
    today        = str(date.today())
    # Possible attendance statuses
    STATUSES = ["Present", "Absent", "Late", "Excused"]
    
    # Create the dashboard window 
    win = tk.Toplevel()
    win.title("Teacher Dashboard")
    win.geometry("800x600")
    win.config(bg="#f0f0f0")
    win.protocol("WM_DELETE_WINDOW", lambda: _logout(win, logout_callback))


    # TOP BAR
    topBar = tk.Frame(win, bg="#1d4ed8", height=50)
    topBar.pack(fill="x")
    topBar.pack_propagate(False)

    tk.Label(
        topBar, text=f"Teacher Dashboard — {username}  |  Today: {today}",
        font=("Arial", 13, "bold"), bg="#1d4ed8", fg="white"
    ).pack(side="left", padx=10, pady=10)

    tk.Button(
        topBar, text="Logout", bg="#dc2626", fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: _logout(win, logout_callback)
    ).pack(side="right", padx=10, pady=8)


    # NOTEBOOK TABS
    tabs = ttk.Notebook(win)
    tabs.pack(fill="both", expand=True, padx=10, pady=10)

    tabStudents   = tk.Frame(tabs, bg="#f0f0f0")
    tabAttendance = tk.Frame(tabs, bg="#f0f0f0")
    tabRecords    = tk.Frame(tabs, bg="#f0f0f0")

    tabs.add(tabStudents,   text="  Students  ")
    tabs.add(tabAttendance, text="  Attendance  ")
    tabs.add(tabRecords,    text="  Records  ")

    
    # STUDENT MANAGEMENT TAB

    # Student table
    stuCols = ("Student ID", "Full Name", "Section")
    stuTable = ttk.Treeview(tabStudents, columns=stuCols, show="headings", height=10)
    for c in stuCols:
        stuTable.heading(c, text=c)
        stuTable.column(c, width=200, anchor="center")
    stuTable.pack(fill="x", padx=10, pady=10)

    # Add student form
    addFrame = tk.LabelFrame(tabStudents, text="Add Student", bg="#f0f0f0",font=("Arial", 10, "bold"))
    addFrame.pack(fill="x", padx=10, pady=5)

    stuEntries = {}
    for i, label in enumerate(["Student ID", "Full Name", "Section"]):
        tk.Label(addFrame, text=label + ":", bg="#f0f0f0").grid(
            row=0, column=i * 2, padx=5, pady=8, sticky="w")
        e = tk.Entry(addFrame, width=20)
        e.grid(row=0, column=i * 2 + 1, padx=5, pady=8)
        stuEntries[label] = e

    def addStudent():
        sid  = stuEntries["Student ID"].get().strip()
        name = stuEntries["Full Name"].get().strip()
        sec  = stuEntries["Section"].get().strip()
        if not (sid and name and sec):
            messagebox.showwarning("Missing", "All fields are required.")
            return
        if any(s["id"] == sid for s in students):
            messagebox.showerror("Error", "Student ID already exists.")
            return
        students.append({"id": sid, "name": name, "section": sec})
        today_status[sid] = "—"
        stuTable.insert("", "end", values=(sid, name, sec))
        for e in stuEntries.values():
            e.delete(0, "end")
        refreshAttTable()

    def deleteStudent():
        sel = stuTable.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Select a student to delete.")
            return
        sid = stuTable.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete student {sid}?"):
            students[:] = [s for s in students if s["id"] != str(sid)]
            today_status.pop(str(sid), None)
            stuTable.delete(sel[0])
            refreshAttTable()

    btnRow = tk.Frame(tabStudents, bg="#f0f0f0")
    btnRow.pack(pady=5)

    tk.Button(btnRow, text="Add Student",    bg="#16a34a", fg="white", width=15, command=addStudent).pack(side="left", padx=5)
    tk.Button(btnRow, text="Delete Student", bg="#dc2626", fg="white", width=15, command=deleteStudent).pack(side="left", padx=5)

    
    # STUDENT ATTENDANCE TAB

    tk.Label(tabAttendance, text=f"Mark Attendance — {today}", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=8)

    attFrame = tk.Frame(tabAttendance, bg="#f0f0f0")
    attFrame.pack(fill="both", expand=True, padx=10)

    statusVars = {}   # {student_id: StringVar}
    attWidgets = []   # keep track of rows to rebuild

    def refreshAttTable():
        for w in attWidgets:
            w.destroy()
        attWidgets.clear()
        statusVars.clear()

        for i, s in enumerate(students):
            lbl = tk.Label(attFrame, text=f"{s['id']}  —  {s['name']}  ({s['section']})", bg="#f0f0f0", font=("Arial", 10), width=35, anchor="w")
            lbl.grid(row=i, column=0, padx=10, pady=4, sticky="w")

            var = tk.StringVar(value=today_status.get(s["id"], "—"))
            statusVars[s["id"]] = var

            menu = tk.OptionMenu(attFrame, var, *STATUSES)
            menu.config(width=10)
            menu.grid(row=i, column=1, padx=10, pady=4)

            attWidgets.extend([lbl, menu])

    def saveAttendance():
        if not students:
            messagebox.showwarning("Empty", "No students to save.")
            return
        for s in students:
            val = statusVars.get(s["id"])
            status = val.get() if val else "—"
            if status == "—":
                messagebox.showwarning("Unmarked",
                    f"Please mark attendance for {s['name']}.")
                return
            today_status[s["id"]] = status

        for s in students:
            records.append({
                "date": today, "id": s["id"], "name": s["name"],
                "section": s["section"], "status": today_status[s["id"]]
            })
        refreshRecords()
        messagebox.showinfo("Saved", f"Attendance saved for {len(students)} student(s).")

    tk.Button(tabAttendance, text="Save Attendance", bg="#1d4ed8", fg="white", font=("Arial", 11, "bold"), width=20, command=saveAttendance).pack(pady=10)


    # ATTENDANCE RECORDS TAB

    recCols = ("Date", "Student ID", "Full Name", "Section", "Status")
    recTable = ttk.Treeview(tabRecords, columns=recCols, show="headings", height=14)
    for c in recCols:
        recTable.heading(c, text=c)
        recTable.column(c, width=130, anchor="center")
    recTable.pack(fill="both", expand=True, padx=10, pady=10)

    def refreshRecords():
        recTable.delete(*recTable.get_children())
        for r in records:
            recTable.insert("", "end", values=(r["date"], r["id"], r["name"], r["section"], r["status"]))

    def exportCSV():
        if not records:
            messagebox.showwarning("Empty", "No records to export.")
            return
        fname = f"attendance_{today}.csv"
        with open(fname, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Date", "Student ID", "Name", "Section", "Status"])
            for r in records:
                w.writerow([r["date"], r["id"], r["name"], r["section"], r["status"]])
        messagebox.showinfo("Exported", f"Saved as: {fname}")

    def showSummary():
        if not records:
            messagebox.showwarning("Empty", "No records saved yet.")
            return
        total   = len(records)
        present = sum(1 for r in records if r["status"] == "Present")
        absent  = sum(1 for r in records if r["status"] == "Absent")
        late    = sum(1 for r in records if r["status"] == "Late")
        excused = sum(1 for r in records if r["status"] == "Excused")
        rate    = round(present / total * 100, 1)
        messagebox.showinfo("Summary",
            f"Total Records : {total}\n"
            f"Present       : {present}\n"
            f"Absent        : {absent}\n"
            f"Late          : {late}\n"
            f"Excused       : {excused}\n"
            f"Attendance    : {rate}%"
        )

    recBtns = tk.Frame(tabRecords, bg="#f0f0f0")
    recBtns.pack(pady=5)

    tk.Button(recBtns, text="Export CSV",   bg="#16a34a", fg="white", width=15, command=exportCSV).pack(side="left", padx=5)
    tk.Button(recBtns, text="Show Summary", bg="#1d4ed8", fg="white", width=15, command=showSummary).pack(side="left", padx=5)


# Helper function to handle logout and window close
def _logout(win, logout_callback):
    win.destroy()
    logout_callback()
