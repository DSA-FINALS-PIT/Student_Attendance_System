import tkinter as tk
from tkinter import messagebox, simpledialog

# =========================================================
# ADMIN INFORMATION SYSTEM - TKINTER VERSION
# =========================================================

admins = []

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Admin Information System")
root.geometry("700x650")
root.config(bg="#f0f0f0")

# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    root,
    text="ADMIN INFORMATION SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#f0f0f0"
)

title.pack(pady=10)

# =========================================================
# INPUT FRAME
# =========================================================

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

# =========================================================
# LABELS AND ENTRIES
# =========================================================

labels = [
    "Admin ID",
    "Full Name",
    "Role",
    "Contact",
    "Email",
    "Username",
    "Password",
    "Access Level"
]

entries = {}

for i, label in enumerate(labels):

    tk.Label(
        frame,
        text=label + ":",
        font=("Arial", 11),
        bg="#f0f0f0"
    ).grid(row=i, column=0, sticky="w", pady=5)

    entry = tk.Entry(frame, width=40)

    if label == "Password":
        entry.config(show="*")

    entry.grid(row=i, column=1, pady=5)

    entries[label] = entry

# =========================================================
# OUTPUT BOX
# =========================================================

output = tk.Text(root, width=80, height=15)
output.pack(pady=15)

# =========================================================
# CLEAR OUTPUT
# =========================================================

def clearOutput():
    output.delete(1.0, tk.END)

# =========================================================
# ADD ADMIN
# =========================================================

def addAdmin():

    adminId = entries["Admin ID"].get().strip()
    fullName = entries["Full Name"].get().strip()
    role = entries["Role"].get().strip()
    contact = entries["Contact"].get().strip()
    email = entries["Email"].get().strip()
    username = entries["Username"].get().strip()
    password = entries["Password"].get().strip()
    access = entries["Access Level"].get().strip()

    # Validate empty fields
    if (
        not adminId or
        not fullName or
        not role or
        not contact or
        not email or
        not username or
        not password or
        not access
    ):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Check duplicate ID
    for admin in admins:
        if admin["id"] == adminId:
            messagebox.showerror("Error", "Admin ID already exists.")
            return

    # Save admin
    admins.append({
        "id": adminId,
        "name": fullName,
        "role": role,
        "contact": contact,
        "email": email,
        "username": username,
        "password": password,
        "access": access
    })

    messagebox.showinfo("Success", f"Admin '{fullName}' added successfully.")

    clearEntries()

# =========================================================
# VIEW ADMINS
# =========================================================

def viewAdmins():

    clearOutput()

    if not admins:
        output.insert(tk.END, "No admin records found.\n")
        return

    for admin in admins:

        output.insert(
            tk.END,
            f"""
----------------------------------------
Admin ID      : {admin['id']}
Full Name     : {admin['name']}
Role          : {admin['role']}
Contact       : {admin['contact']}
Email         : {admin['email']}
Username      : {admin['username']}
Access Level  : {admin['access']}
----------------------------------------

"""
        )

# =========================================================
# DELETE ADMIN
# =========================================================

def deleteAdmin():

    adminId = simpledialog.askstring(
        "Delete Admin",
        "Enter Admin ID to delete:"
    )

    if not adminId:
        return

    for admin in admins:

        if admin["id"] == adminId:

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete admin '{admin['name']}'?"
            )

            if confirm:
                admins.remove(admin)
                messagebox.showinfo(
                    "Success",
                    "Admin deleted successfully."
                )

            return

    messagebox.showerror("Error", "Admin not found.")

# =========================================================
# SEARCH ADMIN
# =========================================================

def searchAdmin():

    keyword = simpledialog.askstring(
        "Search Admin",
        "Enter Admin ID or Name:"
    )

    if not keyword:
        return

    keyword = keyword.lower()

    clearOutput()

    found = False

    for admin in admins:

        if (
            keyword in admin["id"].lower() or
            keyword in admin["name"].lower()
        ):

            found = True

            output.insert(
                tk.END,
                f"""
----------------------------------------
Admin ID      : {admin['id']}
Full Name     : {admin['name']}
Role          : {admin['role']}
Contact       : {admin['contact']}
Email         : {admin['email']}
Username      : {admin['username']}
Access Level  : {admin['access']}
----------------------------------------

"""
            )

    if not found:
        output.insert(tk.END, "No matching admin found.\n")

# =========================================================
# UPDATE ADMIN
# =========================================================

def updateAdmin():

    adminId = simpledialog.askstring(
        "Update Admin",
        "Enter Admin ID to update:"
    )

    if not adminId:
        return

    for admin in admins:

        if admin["id"] == adminId:

            newName = simpledialog.askstring(
                "Update Name",
                f"New Name ({admin['name']}):"
            )

            newRole = simpledialog.askstring(
                "Update Role",
                f"New Role ({admin['role']}):"
            )

            if newName:
                admin["name"] = newName

            if newRole:
                admin["role"] = newRole

            messagebox.showinfo(
                "Success",
                "Admin updated successfully."
            )

            return

    messagebox.showerror("Error", "Admin not found.")

# =========================================================
# ADMIN LOGIN
# =========================================================

def adminLogin():

    username = simpledialog.askstring(
        "Admin Login",
        "Username:"
    )

    password = simpledialog.askstring(
        "Admin Login",
        "Password:",
        show="*"
    )

    if not username or not password:
        return

    for admin in admins:

        if (
            admin["username"] == username and
            admin["password"] == password
        ):

            messagebox.showinfo(
                "Login Success",
                f"Welcome, {admin['name']}!"
            )

            return

    messagebox.showerror(
        "Login Failed",
        "Invalid username or password."
    )

# =========================================================
# CLEAR INPUT FIELDS
# =========================================================

def clearEntries():

    for entry in entries.values():
        entry.delete(0, tk.END)

# =========================================================
# BUTTON FRAME
# =========================================================

buttonFrame = tk.Frame(root, bg="#f0f0f0")
buttonFrame.pack(pady=10)

# =========================================================
# BUTTONS
# =========================================================

tk.Button(
    buttonFrame,
    text="Add Admin",
    width=15,
    command=addAdmin
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    buttonFrame,
    text="View Admins",
    width=15,
    command=viewAdmins
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    buttonFrame,
    text="Update Admin",
    width=15,
    command=updateAdmin
).grid(row=0, column=2, padx=5, pady=5)

tk.Button(
    buttonFrame,
    text="Delete Admin",
    width=15,
    command=deleteAdmin
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    buttonFrame,
    text="Search Admin",
    width=15,
    command=searchAdmin
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    buttonFrame,
    text="Admin Login",
    width=15,
    command=adminLogin
).grid(row=1, column=2, padx=5, pady=5)

tk.Button(
    root,
    text="Exit",
    width=20,
    bg="red",
    fg="white",
    command=root.destroy
).pack(pady=10)

# =========================================================
# RUN PROGRAM
# =========================================================

root.mainloop()