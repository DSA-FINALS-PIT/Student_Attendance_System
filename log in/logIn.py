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
        file.write("admin,admin123,Admin\n")

# -----------------------------------
# LOAD ACCOUNTS FROM TXT FILE
# -----------------------------------
def load_accounts():

    accounts = {}

    with open(DATABASE_FILE, "r") as file:

        for line in file:

            data = line.strip().split(",")

            if len(data) == 3:

                username = data[0]
                password = data[1]
                role = data[2]

                accounts[username] = {
                    "password": password,
                    "role": role
                }

    return accounts

# -----------------------------------
# SAVE NEW ACCOUNT TO TXT FILE
# -----------------------------------
def save_account(username, password, role):

    with open(DATABASE_FILE, "a") as file:

        file.write(f"{username},{password},{role}\n")

# -----------------------------------
# LOGIN FUNCTION
# -----------------------------------
def login():

    username = username_entry.get()
    password = password_entry.get()

    accounts = load_accounts()

    if username in accounts:

        if accounts[username]["password"] == password:

            role = accounts[username]["role"]

            messagebox.showinfo(
                "Login Successful",
                f"Welcome {username}!\nRole: {role}"
            )

        else:
            messagebox.showerror(
                "Error",
                "Incorrect password!"
            )

    else:
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
    create_window.geometry("300x300")

    # Username
    tk.Label(
        create_window,
        text="Username"
    ).pack(pady=5)

    new_username = tk.Entry(create_window)
    new_username.pack()

    # Password
    tk.Label(
        create_window,
        text="Password"
    ).pack(pady=5)

    new_password = tk.Entry(
        create_window,
        show="*"
    )
    new_password.pack()

    # Role
    tk.Label(
        create_window,
        text="Role"
    ).pack(pady=5)

    role_var = tk.StringVar(value="Student")

    tk.OptionMenu(
        create_window,
        role_var,
        "Admin",
        "Teacher",
        "Student"
    ).pack()

    # Save Account
    def register_account():

        username = new_username.get()
        password = new_password.get()
        role = role_var.get()

        if username == "" or password == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields!"
            )
            return

        accounts = load_accounts()

        if username in accounts:

            messagebox.showerror(
                "Error",
                "Username already exists!"
            )
            return

        save_account(username, password, role)

        messagebox.showinfo(
            "Success",
            "Account created successfully!"
        )

        create_window.destroy()

    tk.Button(
        create_window,
        text="Create Account",
        bg="green",
        fg="white",
        command=register_account
    ).pack(pady=15)

# -----------------------------------
# FORGOT PASSWORD WINDOW
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

        accounts = load_accounts()

        if username in accounts:

            password = accounts[username]["password"]

            messagebox.showinfo(
                "Recovered Password",
                f"Username: {username}\nPassword: {password}"
            )

        else:

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

# Title
tk.Label(
    root,
    text="LOGIN SYSTEM",
    font=("Arial", 18, "bold")
).pack(pady=20)

# Username
tk.Label(
    root,
    text="Username"
).pack()

username_entry = tk.Entry(
    root,
    width=30
)
username_entry.pack(pady=5)

# Password
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

# Login Button
tk.Button(
    root,
    text="Login",
    width=20,
    bg="blue",
    fg="white",
    command=login
).pack(pady=15)

# Forgot Password Button
tk.Button(
    root,
    text="Forgot Password",
    width=20,
    command=forgot_password
).pack(pady=5)

# Create Account Button
tk.Button(
    root,
    text="Create Account",
    width=20,
    command=create_account
).pack(pady=5)

# Run Program
root.mainloop()