import tkinter as tk
from tkinter import messagebox
import os

# -----------------------------------
# DATABASE FILE
# -----------------------------------
DATABASE_FILE = "accounts.txt"

# -----------------------------------
# CREATE FILE IF NOT EXISTS
# -----------------------------------
if not os.path.exists(DATABASE_FILE):

    with open(DATABASE_FILE, "w") as file:
        file.write("")

# -----------------------------------
# LOGIN FUNCTION
# -----------------------------------
def login():

    username = username_entry.get()
    password = password_entry.get()

    found = False

    with open(DATABASE_FILE, "r") as file:

        for line in file:

            data = line.strip().split(",")

            if len(data) >= 3:

                stored_username = data[-3]
                stored_password = data[-2]
                role = data[-1]

                if username == stored_username:

                    found = True

                    if password == stored_password:

                        messagebox.showinfo(
                            "Login Successful",
                            f"Welcome {username}\nRole: {role}"
                        )

                    else:
                        messagebox.showerror(
                            "Error",
                            "Incorrect Password!"
                        )

    if not found:

        messagebox.showerror(
            "Error",
            "Username not found!"
        )

# -----------------------------------
# CREATE ACCOUNT WINDOW
# -----------------------------------
def create_account():

    create_window = tk.Toplevel(root)

    create_window.title("Create Account")
    create_window.geometry("500x700")

    role_var = tk.StringVar(value="Student")

    # -----------------------------------
    # ROLE SELECTION
    # -----------------------------------
    tk.Label(
        create_window,
        text="Select Role",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    tk.OptionMenu(
        create_window,
        role_var,
        "Student",
        "Teacher",
        "Admin"
    ).pack()

    form_frame = tk.Frame(create_window)
    form_frame.pack(pady=10)

    entries = {}

    # -----------------------------------
    # GENERATE FORM
    # -----------------------------------
    def generate_form(*args):

        for widget in form_frame.winfo_children():
            widget.destroy()

        entries.clear()

        role = role_var.get()

        # -----------------------------------
        # STUDENT FORM
        # -----------------------------------
        if role == "Student":

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
                "Password"
            ]

        # -----------------------------------
        # TEACHER FORM
        # -----------------------------------
        elif role == "Teacher":

            fields = [
                "Teacher ID",
                "Full Name",
                "Section",
                "Assigned Subjects",
                "Contact Number",
                "Email Address",
                "Username",
                "Password"
            ]

        # -----------------------------------
        # ADMIN FORM
        # -----------------------------------
        else:

            fields = [
                "Admin ID",
                "Full Name",
                "Position/Role",
                "Contact Number",
                "Email Address",
                "Username",
                "Password"
            ]

        # -----------------------------------
        # CREATE LABELS AND ENTRIES
        # -----------------------------------
        for field in fields:

            tk.Label(
                form_frame,
                text=field
            ).pack()

            if field == "Password":

                entry = tk.Entry(
                    form_frame,
                    width=40,
                    show="*"
                )

            else:

                entry = tk.Entry(
                    form_frame,
                    width=40
                )

            entry.pack(pady=3)

            entries[field] = entry

    role_var.trace("w", generate_form)

    generate_form()

    # -----------------------------------
    # REGISTER ACCOUNT
    # -----------------------------------
        # -----------------------------------
    # REGISTER ACCOUNT
    # -----------------------------------
    def register_account():

        role = role_var.get()

        values = []

        for field, entry in entries.items():

            value = entry.get()

            if value == "":

                messagebox.showwarning(
                    "Warning",
                    "Please fill all fields!"
                )
                return

            values.append(value)

        username = entries["Username"].get()

        # -----------------------------------
        # CHECK DUPLICATE USERNAME
        # -----------------------------------
        with open(DATABASE_FILE, "r") as file:

            for line in file:

                data = line.strip().split(",")

                if len(data) >= 3:

                    stored_username = data[-3]

                    if username == stored_username:

                        messagebox.showerror(
                            "Error",
                            "Username already exists!"
                        )
                        return

        # -----------------------------------
        # SAVE PERSONAL INFO
        # -----------------------------------
        save_personal_info(role, values)

        # -----------------------------------
        # SAVE ACCOUNT
        # -----------------------------------
        with open(DATABASE_FILE, "a") as file:

            file.write(",".join(values) + f",{role}\n")

        messagebox.showinfo(
            "Success",
            "Request to create account submitted!"
        )

        create_window.destroy()

    # -----------------------------------
    # CREATE ACCOUNT BUTTON
    # -----------------------------------
    tk.Button(
        create_window,
        text="Submit Request Create Account",
        bg="green",
        fg="white",
        width=30,
        command=register_account
    ).pack(pady=15)
        # -----------------------------------
# PERSONAL INFORMATION DATABASE FILE
# -----------------------------------
INFO_DATABASE_FILE = "personal_info.txt"

# -----------------------------------
# CREATE FILE IF NOT EXISTS
# -----------------------------------
if not os.path.exists(INFO_DATABASE_FILE):

    with open(INFO_DATABASE_FILE, "w") as file:
        file.write("")

# -----------------------------------
# SAVE PERSONAL INFORMATION
# -----------------------------------
def save_personal_info(role, values):

    with open(INFO_DATABASE_FILE, "a") as file:

        # STUDENT
        if role == "Student":

            file.write(
                f"""
========================================
ROLE: Student
Student ID: {values[0]}
Full Name: {values[1]}
Course/Program: {values[2]}
Year & Section: {values[3]}
Gender: {values[4]}
Birthdate: {values[5]}
Contact Number: {values[6]}
Email Address: {values[7]}
Address: {values[8]}
Username: {values[9]}
========================================
"""
            )

        # TEACHER
        elif role == "Teacher":

            file.write(
                f"""
========================================
ROLE: Teacher
Teacher ID: {values[0]}
Full Name: {values[1]}
Section: {values[2]}
Assigned Subjects: {values[3]}
Contact Number: {values[4]}
Email Address: {values[5]}
Username: {values[6]}
========================================
"""
            )

        # ADMIN
        elif role == "Admin":

            file.write(
                f"""
========================================
ROLE: Admin
Admin ID: {values[0]}
Full Name: {values[1]}
Position/Role: {values[2]}
Contact Number: {values[3]}
Email Address: {values[4]}
Username: {values[5]}
========================================
"""
            )

        # -----------------------------------
        # SAVE TO TXT FILE
        # -----------------------------------
        with open(DATABASE_FILE, "a") as file:

            file.write(",".join(values) + f",{role}\n")

        messagebox.showinfo(
            "Success",
            "Request to create account submitted!"
        )

        create_window.destroy()

    # -----------------------------------
    # CREATE ACCOUNT BUTTON
    # -----------------------------------
    tk.Button(
        create_window,
        text="Create Account",
        bg="green",
        fg="white",
        width=20,
        command=register_account
    ).pack(pady=15)

# -----------------------------------
# FORGOT PASSWORD
# -----------------------------------
def forgot_password():

    forgot_window = tk.Toplevel(root)

    forgot_window.title("Forgot Password")
    forgot_window.geometry("300x200")

    tk.Label(
        forgot_window,
        text="Enter Username"
    ).pack(pady=10)

    forgot_username = tk.Entry(forgot_window)
    forgot_username.pack()

    def recover_password():

        username = forgot_username.get()

        found = False

        with open(DATABASE_FILE, "r") as file:

            for line in file:

                data = line.strip().split(",")

                if len(data) >= 3:

                    stored_username = data[-3]
                    stored_password = data[-2]

                    if username == stored_username:

                        found = True

                        messagebox.showinfo(
                            "Recovered Password",
                            f"Password: {stored_password}"
                        )

        if not found:

            messagebox.showerror(
                "Error",
                "Username not found!"
            )

    tk.Button(
        forgot_window,
        text="Recover Password",
        bg="orange",
        command=recover_password
    ).pack(pady=15)

# -----------------------------------
# MAIN WINDOW
# -----------------------------------
root = tk.Tk()

root.title("Student Attendance System")
root.geometry("400x350")
root.resizable(False, False)

# -----------------------------------
# TITLE
# -----------------------------------
tk.Label(
    root,
    text="LOGIN SYSTEM",
    font=("Arial", 18, "bold")
).pack(pady=20)

# -----------------------------------
# USERNAME
# -----------------------------------
tk.Label(
    root,
    text="Username"
).pack()

username_entry = tk.Entry(
    root,
    width=30
)
username_entry.pack(pady=5)

# -----------------------------------
# PASSWORD
# -----------------------------------
tk.Label(
    root,
    text="Password"
).pack()

password_entry = tk.Entry(
    root,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

# -----------------------------------
# LOGIN BUTTON
# -----------------------------------
tk.Button(
    root,
    text="Login",
    width=20,
    bg="blue",
    fg="white",
    command=login
).pack(pady=15)

# -----------------------------------
# FORGOT PASSWORD BUTTON
# -----------------------------------
tk.Button(
    root,
    text="Forgot Password",
    width=20,
    command=forgot_password
).pack(pady=5)

# -----------------------------------
# CREATE ACCOUNT BUTTON
# -----------------------------------
tk.Button(
    root,
    text="Create Account",
    width=20,
    command=create_account
).pack(pady=5)

# -----------------------------------
# RUN PROGRAM
# -----------------------------------
root.mainloop()