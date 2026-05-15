# =========================================================
# ADMIN INFORMATION SYSTEM
# Console-Based Python Program
# =========================================================

# Store admins as a list of dictionaries
admins = []


# =========================================================
# ADD ADMIN
# =========================================================

def addAdmin():

    print("\n========== ADD ADMIN ==========")

    adminId = input("Enter Admin ID: ").strip()
    fullName = input("Enter Full Name: ").strip()
    role = input("Enter Position / Role: ").strip()
    contact = input("Enter Contact Number: ").strip()
    email = input("Enter Email Address: ").strip()
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    access = input("Enter Access Level: ").strip()

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
        print("\n[ERROR] Please fill in all fields.")
        return

    # Check duplicate admin ID
    for admin in admins:
        if admin["id"] == adminId:
            print("\n[ERROR] Admin ID already exists.")
            return

    # Store admin information
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

    print(f"\n[SUCCESS] Admin '{fullName}' added successfully.")


# =========================================================
# VIEW ADMINS
# =========================================================

def viewAdmins():

    print("\n========== ADMIN LIST ==========")

    if not admins:
        print("No admin records found.")
        return

    for admin in admins:
        print(f"""
----------------------------------------
Admin ID      : {admin['id']}
Full Name     : {admin['name']}
Role          : {admin['role']}
Contact       : {admin['contact']}
Email          : {admin['email']}
Username      : {admin['username']}
Access Level  : {admin['access']}
----------------------------------------
""")


# =========================================================
# DELETE ADMIN
# =========================================================

def deleteAdmin():

    print("\n========== DELETE ADMIN ==========")

    adminId = input("Enter Admin ID to delete: ").strip()

    for admin in admins:

        if admin["id"] == adminId:

            confirm = input(
                f"Delete admin '{admin['name']}'? (yes/no): "
            ).lower()

            if confirm == "yes":
                admins.remove(admin)
                print("\n[SUCCESS] Admin deleted successfully.")
            else:
                print("\nDelete cancelled.")

            return

    print("\n[ERROR] Admin not found.")


# =========================================================
# SEARCH ADMIN
# =========================================================

def searchAdmin():

    print("\n========== SEARCH ADMIN ==========")

    keyword = input("Enter Admin ID or Name: ").lower().strip()

    found = False

    for admin in admins:

        if (
            keyword in admin["id"].lower() or
            keyword in admin["name"].lower()
        ):

            found = True

            print(f"""
----------------------------------------
Admin ID      : {admin['id']}
Full Name     : {admin['name']}
Role          : {admin['role']}
Contact       : {admin['contact']}
Email         : {admin['email']}
Username      : {admin['username']}
Access Level  : {admin['access']}
----------------------------------------
""")

    if not found:
        print("\n[ERROR] No matching admin found.")


# =========================================================
# UPDATE ADMIN
# =========================================================

def updateAdmin():

    print("\n========== UPDATE ADMIN ==========")

    adminId = input("Enter Admin ID to update: ").strip()

    for admin in admins:

        if admin["id"] == adminId:

            print("\nLeave blank if no changes.\n")

            newName = input(f"Full Name ({admin['name']}): ").strip()
            newRole = input(f"Role ({admin['role']}): ").strip()
            newContact = input(f"Contact ({admin['contact']}): ").strip()
            newEmail = input(f"Email ({admin['email']}): ").strip()
            newUsername = input(f"Username ({admin['username']}): ").strip()
            newPassword = input("New Password: ").strip()
            newAccess = input(f"Access Level ({admin['access']}): ").strip()

            if newName:
                admin["name"] = newName

            if newRole:
                admin["role"] = newRole

            if newContact:
                admin["contact"] = newContact

            if newEmail:
                admin["email"] = newEmail

            if newUsername:
                admin["username"] = newUsername

            if newPassword:
                admin["password"] = newPassword

            if newAccess:
                admin["access"] = newAccess

            print("\n[SUCCESS] Admin information updated.")
            return

    print("\n[ERROR] Admin not found.")


# =========================================================
# LOGIN SYSTEM
# =========================================================

def adminLogin():

    print("\n========== ADMIN LOGIN ==========")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for admin in admins:

        if (
            admin["username"] == username and
            admin["password"] == password
        ):

            print(f"\nWelcome, {admin['name']}!")
            return

    print("\n[ERROR] Invalid username or password.")


# =========================================================
# MAIN MENU
# =========================================================

def mainMenu():

    while True:

        print("""
=================================================
        ADMIN INFORMATION SYSTEM
=================================================
[1] Add Admin
[2] View Admins
[3] Update Admin
[4] Delete Admin
[5] Search Admin
[6] Admin Login
[7] Exit
=================================================
""")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            addAdmin()

        elif choice == "2":
            viewAdmins()

        elif choice == "3":
            updateAdmin()

        elif choice == "4":
            deleteAdmin()

        elif choice == "5":
            searchAdmin()

        elif choice == "6":
            adminLogin()

        elif choice == "7":
            print("\nSystem closed.")
            break

        else:
            print("\n[ERROR] Invalid choice.")


# =========================================================
# RUN SYSTEM
# =========================================================

mainMenu()


