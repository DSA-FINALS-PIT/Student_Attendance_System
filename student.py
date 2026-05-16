import tkinter as tk
from tkinter import ttk, messagebox

# STORAGE
students = []

# MAIN WINDOW
window = tk.Tk()
window.title("Student Information System")
window.geometry("1250x700")
window.config(bg="#f0f4f8")

# TOP BAR
topBar = tk.Frame(window, bg="#2563eb", height=55)
topBar.pack(fill="x")
topBar.pack_propagate(False)

tk.Label(
    topBar,
    text="📚 Student Information System",
    font=("Arial", 16, "bold"),
    bg="#2563eb",
    fg="white"
).pack(side="left", padx=10, pady=12)

# NOTEBOOK
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 11), padding=[12, 6])

tabs = ttk.Notebook(window)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

tabStudents = tk.Frame(tabs, bg="#f0f4f8")
tabs.add(tabStudents, text=" Students")

# TABLE
columns = (
    "Student ID",
    "Full Name",
    "Course/Program",
    "Year & Section",
    "Gender",
    "Birthdate",
    "Contact Number",
    "Email Address",
    "Address",
    "Username",
    "Password",
    "Teacher",
    "Teacher ID",
    "Section",
    "Subject"
)

table = ttk.Treeview(tabStudents, columns=columns, show="headings", height=10)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120, anchor="center")

table.pack(fill="x", padx=10, pady=10)

# ADD BOARD
addBoard = tk.LabelFrame(
    tabStudents,
    text="➕ Add Student Information",
    font=("Arial", 11, "bold"),
    bg="#f0f4f8"
)
addBoard.pack(fill="x", padx=10, pady=10)

# INPUT FIELDS
entries = {}

fields = [
    "Student ID",
    "Full Name",
    "Course/Program",
    "Year & Section",
    "Gender",
    "Birthdate",
    "Contact Number",
    "Email Address",
    "Address",
    "Username",
    "Password",
    "Teacher",
    "Teacher ID",
    "Section",
    "Subject"
]

row = 0
col = 0

for field in fields:
    tk.Label(addBoard, text=field + ":", bg="#f0f4f8").grid(
        row=row, column=col, sticky="w", padx=5, pady=5
    )

    entry = tk.Entry(addBoard, width=20,
                     show="*" if field == "Password" else "")
    entry.grid(row=row, column=col+1, padx=5, pady=5)

    entries[field] = entry

    col += 2
    if col > 2:
        col = 0
        row += 1


# FUNCTIONS
def addStudent():
    values = [entries[f].get().strip() for f in fields]

    if values[0] == "" or values[1] == "":
        messagebox.showwarning("Missing Data", "Student ID and Full Name are required!")
        return

    table.insert("", "end", values=values)

    for e in entries.values():
        e.delete(0, "end")

    messagebox.showinfo("Success", "Student Added Successfully!")


def deleteStudent():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("No Selection", "Please select a student!")
        return

    table.delete(selected[0])


def clearFields():
    for e in entries.values():
        e.delete(0, "end")


# BUTTONS (INSIDE ADD BOARD)
btnFrame = tk.Frame(addBoard, bg="#f0f4f8")
btnFrame.grid(row=row+1, column=0, columnspan=4, pady=10, sticky="w")

tk.Button(btnFrame,
          text="➕ ADD STUDENT",
          command=addStudent,
          bg="#16a34a",
          fg="white",
          font=("Arial", 12, "bold"),
          padx=20,
          pady=8).pack(side="left", padx=5)

tk.Button(btnFrame,
          text="🗑 DELETE",
          command=deleteStudent,
          bg="#dc2626",
          fg="white",
          font=("Arial", 10, "bold"),
          padx=10,
          pady=6).pack(side="left", padx=5)

tk.Button(btnFrame,
          text="🧹 CLEAR",
          command=clearFields,
          bg="#2563eb",
          fg="white",
          font=("Arial", 10, "bold"),
          padx=10,
          pady=6).pack(side="left", padx=5)

# RUN
window.mainloop()
