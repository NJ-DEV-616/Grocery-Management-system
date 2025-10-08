# project.py

# ================== Imports ==================
import re
import json
import os
import sys
from tabulate import tabulate
from datetime import datetime

# ================== Constants ==================
USERS_FILE = 'users.json'
ITEMS_FILE = 'items.json'
BILLS_FILE = 'bills.json'

# ================== Helper Functions ==================
def load_data(filename:str) -> list:
    '''
    Loads JSON data from file.
    If file does not exist or is empty, returns an empty list.
    '''

    # If file exists, load existing data
    if os.path.exists(filename):
        with open (filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(filename : str, data: list):
    """
    Save list data as JSON to a file with pretty formatting.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def print_proper_bill(user_name: str, bill: dict):
    """
    Prints a formatted bill using tabulate.
    """
    print("\n======== 🧾Bill ========")
    print(f"Customer: {user_name}")
    print(f"Date    : {bill['date']}")

    table = [
        [i, item["name"], item["quantity"], item["unit"], item["price"], item["total"]]
        for i, item in enumerate(bill["items"], start=1)
    ]
    headers = ["S.N.", "Item", "Qty", "Unit", "Rate (Rs.)", "Total (Rs.)"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    print(f"\n💰 Grand Total: Rs.{bill['grand_total']}")
    print("==========================\n")

def get_valid_action(prompt:str,valid_range : range) -> int:
    '''
    Ensures input is a valid integer within a given range.
    Returns the integer chosen.
    '''
    while True:
        try:
            action = int(input(prompt))
            if action in valid_range:
                return action
            else:
                print(f"Please enter a number between {valid_range.start} and {valid_range.stop -1}.")
        except ValueError:
            print("Invalid input. Please enter a number")

def get_amount_and_price(prompt : str, unit : str) -> tuple:
    '''
    Helper function:
    Asks for item quantity and price per unit.
    '''

    while True:
        try:
            amount = float(input(prompt))
            price_per_unit =  float(input(f"Enter price per {unit}: "))
            return amount,price_per_unit
        except ValueError:
            print("Invalid Input. Please Enter numeric values.")

def validate_email_address(email:str) -> bool:
    '''
    Validates email format using regex.
    '''
    pattern = r'^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'

    return True if re.match(pattern, email) else False

def validate_password(password:str) -> bool:
    '''
    Validates password strength.
    Rules:
    - Length: 8–12 characters
    - At least 1 uppercase, 1 lowercase
    - At least 1 number
    - At least 1 special character
    '''

    # password should be 8 to 12 characters long
    if not 12 >= len(password) >= 8:
        return False

    # password must have at least 1 uppercase letter and 1 lowercase letter
    if password == password.lower() or password == password.upper():
        return False

    # password must have at least 1 number
    if not re.search(r'\d', password):
        return False

    # password must have at least 1 special character
    if not re.search(r'[@$!%*?&]', password):
        return False

    # If all the conditions for password are met, it returns True
    return True

# ================== User Management ==================
def signup():
    '''
    Handles user registration.
    - collect name, email and password
    - validates email and password
    - stores user data in users.json
    '''

    name = input("Enter name: ").strip()

    # Validate email format
    while True:
        email = input("Enter email address: ").strip().lower()
        if validate_email_address(email):
            break
        else:
            print("Invalid Email address.\n")

    # Validate Password format
    while True:
        password = input("Enter password: ")
        if not validate_password(password):
            print("❌ Invalid password. Rules:")
            print("   - 8 to 12 characters long")
            print("   - At least one uppercase letter (A–Z)")
            print("   - At least one lowercase letter (a–z)")
            print("   - At least one number (0–9)")
            print("   - At least one special character (@$!%*?&)")
        else:
            break

    # New user data
    new_user = {
            "name" : name,
            "email" : email,
            "password": password,
            "admin": False
        }

    users = load_data(USERS_FILE)

    # Prevents duplicate email registration
    for user in users:
        if user["email"] == email:
            print("⚠️ Email already registered! Please use a different email.")
            return None  # return value makes function testable -> failure case (duplicate email)

    # Add new user
    users.append(new_user)

    # Save updated users list to file
    save_data(USERS_FILE, users)

    print("✅ User signed up successfully!\n")
    return new_user  # return value makes function testable -> success case (user added).

def login():
    '''
    Handles login for both users and admins.
    - Matches email and password.
    - Routes to Admin/user dashboard
    '''

    email = input("Enter email address: ").strip().lower()
    password = input("Enter password: ").strip()
    users = load_data(USERS_FILE)

    # Verify Credentials
    for user in users:
         if user["email"] == email and user["password"] == password :
             if user["admin"] == True:
                print(f"\nWelcome {user['name']}")
                admin_menu(user)
                return user # makes function testable -> success (valid credentials, correct account)
             else:
                print(f"\nWelcome {user['name']}")
                user_menu(user)
                return user # makes function testable -> success (valid credentials, correct account)

    #If no user matches
    print("❌ Invalid email or password.")
    return None # makes funnction testable -> failure (invalid credentials).

# ================== Profile Management ==================
def update_profile(current_user: dict):
    """
    Allows both user and admin to update their profile (name, email, password).
    """
    users = load_data(USERS_FILE)

    print("\n--- Update Profile ---")
    print("1. Change Name")
    print("2. Change Email")
    print("3. Change Password")
    print("4. Back")

    choice = get_valid_action("Enter choice (1-4): ", range(1, 5))

    match choice:
        case 1:
            new_name = input("Enter new name: ").strip()
            current_user["name"] = new_name
            print("✅ Name updated successfully!")

        case 2:
            while True:
                new_email = input("Enter new email: ").strip().lower()
                if not validate_email_address(new_email):
                    print("❌ Invalid email format.")
                    continue
                if any(u['email'] == new_email for u in users if u != current_user):
                    print("⚠️ Email already exists! Try another.")
                    continue
                current_user["email"] = new_email
                print("✅ Email updated successfully!")
                break

        case 3:
            while True:
                new_password = input("Enter new password: ")
                if validate_password(new_password):
                    current_user["password"] = new_password
                    print("✅ Password updated successfully!")
                    break
                else:
                    print("❌ Weak password. Try again.")

    # Save users back
    # ensure current_user object in users list is updated
    for i, u in enumerate(users):
        if u.get("email") == current_user.get("email") or \
        (u.get("name") == current_user.get("name") and u.get("password") == current_user.get("password")):
            users[i] = current_user
            break
    else:
        # If not found, append (defensive)
        users.append(current_user)

    save_data(USERS_FILE, users)
    return True  # return value (True) to make function testable

# ================== Admin Functions ==================
def add_item():
    '''
    Allows admin to add new items to stock.
    Handles:
    - Name
    - Type (count/weight/volume)
    - Amount and rate
    '''

    item_name = input("\nEnter item name: ").title()
    print("\nSelect amount type:")
    print("1. Count (pieces/units)")
    print("2. Weight (kilograms)")
    print("3. volume (litres)")
    choice = get_valid_action("\nEnter choice (1-3): ", range(1,4))
    match choice:
        case 1:
            amount, price = get_amount_and_price("\nEnter number of pieces: ", "piece")
        case 2:
            amount, price = get_amount_and_price("\nEnter weight in kilograms: ", "kg")
        case 3:
            amount, price = get_amount_and_price("\nEnter volume in litres: ", "L")

    new_item = {
        "name": item_name,
        "amount": amount,
        "unit": "pcs" if choice == 1 else ("kg" if choice == 2 else "L"),
        "rate": price
        }

    items = load_data(ITEMS_FILE)

    # Prevent duplicate items
    for item in items:
        if item["name"] == item_name:
            print(f"❌ Item '{item_name}' already exists in the list.")
            return None # return None explicitly for testing

    # Add new item
    items.append(new_item)

    # Save updated stock
    save_data(ITEMS_FILE, items)

    print(f"✅ Item added: {new_item['name']} - {new_item['amount']} {new_item['unit']} @ {new_item['rate']} per {new_item['unit']}")
    return new_item #returns the actual item dict for testing

def update_stock():
    """
    Allows admin to update or delete stock for existing items.
    Features:
    - Update quantity, price, both, name, or delete item.
    - When changing name, optionally update the unit.
    - Undo last update.
    - All updates require confirmation.
    """

    items = load_data(ITEMS_FILE)

    # Backup items for undo
    backup_items = [item.copy() for item in items]

    # Display current stock
    view_items()

    # Select item to update/delete
    item_index = get_valid_action(
        f"Enter the item index to update (1-{len(items)}): ",
        range(1, len(items) + 1)
    )
    item = items[item_index - 1]

    print(f"\nEditing '{item['name']}' (Available: {item['amount']} {item['unit']} @ Rs.{item['rate']}/{item['unit']})")

    # Show update options
    print("1. Update quantity")
    print("2. Update price per unit")
    print("3. Both quantity and price")
    print("4. Update Name")
    print("5. Delete Item")
    choice = get_valid_action("Enter your choice(1-5): ", range(1, 6))

    updated = False

    match choice:
        case 1:
            new_amount = float(input(f"Enter new quantity for {item['name']}(in {item['unit']}): "))
            confirm = input(f"Confirm update quantity to {new_amount} {item['unit']} (y/n): ").strip().lower()
            if confirm == 'y':
                item['amount'] = new_amount
                print(f"✅ Quantity updated to {new_amount} {item['unit']}")
                updated = True
            else:
                print("❌ Update cancelled.")

        case 2:
            new_rate = float(input(f"Enter new price per {item['unit']} for {item['name']}: "))
            confirm = input(f"Confirm update price to Rs.{new_rate}/{item['unit']}? (y/n): ").strip().lower()
            if confirm == "y":
                item["rate"] = new_rate
                print(f"✅ Price updated to Rs.{new_rate} per {item['unit']}")
                updated = True
            else:
                print("❌ Update cancelled.")

        case 3:
            new_amount = float(input(f"Enter new quantity for {item['name']} ({item['unit']}): "))
            new_rate = float(input(f"Enter new price per {item['unit']} for {item['name']}: "))
            confirm = input(f"Confirm update to {new_amount} {item['unit']} @ Rs.{new_rate}/{item['unit']}? (y/n): ").strip().lower()
            if confirm == "y":
                item["amount"] = new_amount
                item["rate"] = new_rate
                print(f"✅ Quantity and Price updated.")
                updated = True
            else:
                print("❌ Update cancelled.")

        case 4:
            new_name = input(f"Enter the new name for {item['name']}: ").title()
            #Ask if unit should be changed
            change_unit = input("Do you also want to change the unit?(y/n): ").strip().lower()
            if change_unit == 'y':
                print("Select new unit: ")
                print("1. count(pcs)")
                print("2. weight(kg)")
                print("3. volume (L)")
                unit_choice = get_valid_action("Enter choice(1-3): ", range(1,4))
                new_unit = 'pcs' if unit_choice == 1 else ('kg' if unit_choice == 2 else 'L')
            else:
                new_unit = item['unit']

            confirm = input(f"Confirm update to name '{new_name} and unit '{new_unit}'? (y/n): ").strip().lower()
            if confirm == 'y':
                item['name'] = new_name
                item['unit'] = new_unit
                print(f"✅ Item name updated to '{new_name}' with unit '{new_unit}'")
                updated = True
            else:
                print("❌ Update cancelled.")

        case 5:
            confirm = input(f"Are you sure want to delete '{item['name']}'? (y/n): ").strip().lower()
            if confirm == 'y':
                items.pop(item_index - 1)
                print(f"🗑️ '{item['name']}' has been deleted.")
                updated = True
            else:
                print("❌ Deletion cancelled.")

    # Save updated stock
    save_data(ITEMS_FILE, items)

    print("\n📦 Updated Stock:")
    view_items()

    # Ask admin if they want to undo last update
    undo = input("\nDo you want to undo the last update? (y/n): ").strip().lower()
    if undo == "y":
        save_data("items.json", backup_items)
        print("↩️ Last update undone.")
        print("\n📦 Stock after undo:")
        view_items()
        updated = True

    return updated  # to make function testable

# ================== User Functions ==================
def buy_item(user_name:str, user_email:str):
    """
    Allows a user to purchase multiple items,updates stock,
    and saves the purchase bill under the user's email in bills.json.
    """

    # Load available items from items.json
    items = load_data(ITEMS_FILE)
    if not items:
        print("❌ No items available.")
        return

    purchased_items = []  # List to store items purchased in this session
    grand_total = 0  # Total cost of all purchased items

    while True:
        # Display all available items
        view_items()

        # Map numeric index to item dictionary for user selection
        items_dict = {i: item for i,item in enumerate(items, start = 1)}

        # Ask user to select an item by index
        item_index = get_valid_action(
            f"Enter the item index(1-{len(items)}): ",
            range(1,len(items)+1)
        )
        item = items_dict[item_index]

        # Check available stock
        max_qty = int(item["amount"])
        if max_qty == 0:
            print(f"❌ {item['name']} is out of stock.")
            continue

        # Ask user for quantity
        quantity = get_valid_action(
            f"Enter the quantity(1-{max_qty} {item['unit']}): ",
            range(1, max_qty+1)
        )

        # Calculate total cost for this item
        total_cost = quantity * item['rate']

        # Add item to purchased items list
        purchased_items.append({
            "name": item['name'],
            "quantity": quantity,
            "unit": item['unit'],
            "price": item['rate'],
            "total": total_cost
        })
        grand_total += total_cost

        # Update stock in memory
        item['amount'] -= quantity

        #Asks if user want to add more items
        more = input("Add more items? (y/n): ").strip().lower()
        if more != 'y':
            break

    # Save updated stock back to items.json
    save_data(ITEMS_FILE, items)

    #Create Bill entry for this purchase
    bill_entry = {
        "date" : datetime.now().strftime("%y-%m-%d %H-%M-%S"),
        "items" : purchased_items,
        "grand_total": grand_total
    }

    # Load existing bills
    bills = load_data(BILLS_FILE)

    # Check if user already exists in bills.json
    user_found = False
    for user in bills:
        if user["email"] == user_email:
            user["bills"].append(bill_entry)
            user_found = True
            break

    # If user not found, create a new entry
    if not user_found:
        bills.append({
            "email": user_email,
            "name": user_name,
            "bills": [bill_entry]
        })

    # Save updated bills back to bills.json
    save_data(BILLS_FILE, bills)

    # Print purchase summary for the user
    print("\n✅ Purchase successful!")
    choice = input("Do you want a proper bill? (y/n): ").strip().lower()
    if choice == "y":
        print_proper_bill(user_name, bill_entry)
    else:
        print(f"Bill for {user_name} on {bill_entry['date']}")
        for item in purchased_items:
            print(f"- {item['name']} x {item['quantity']} {item['unit']} = Rs.{item['total']}")
        print(f"Grand Total = Rs. {grand_total}\n")

    return bill_entry # to make function testable

def view_items():
    '''
    Displays all items in a formatted table using tabulate.
    '''

    items = load_data(ITEMS_FILE)

    if not items:
        print("\n❌ No items found in the store.\n")
        return

    # Build table for display
    table = [
        [i, item["name"], f"{item['amount']} {item['unit']}", item["rate"] ]
        for i, item in enumerate(items, start = 1)
    ]

    headers = ["Index", "Item Name", "Available Stock", "Rate"]
    print("\n📦 Available Items:")
    print(tabulate(table, headers = headers, tablefmt = "fancy_grid"))

def view_purchase_history(user_name: str, user_email: str):
    """
    Display all past purchases for a user, optionally filtered by date.
    """

    bills = load_data(BILLS_FILE)

    # Find the user in bills.json
    user_data = None
    for user in bills:
        if user['email'] == user_email:
            user_data = user
            break

    if not user_data:
        print(f"\n❌ No purchase history found for {user_name}")
        return

    # Ask user if they want to filter by date
    filter_date = input("Enter a date to filter (YYYY-MM-DD) or press Enter to view all: ").strip()

    print(f"\n📜 Purchase history for {user_data['name']} ({user_email})")
    history_found = False

    # Loop through all bills for the user
    for bill in user_data["bills"]:
        bill_date = bill["date"].split(" ")[0]  # Extract YYYY-MM-DD from datetime

        # Skip if filter is applied and does not match
        if filter_date and bill_date != filter_date:
            continue

        history_found = True

        # Print purchased items
        print(f"\n🗓 Date: {bill['date']}")
        for item in bill["items"]:
            print(f"- {item['name']} x {item['quantity']} {item['unit']} = Rs. {item['total']}")
        print(f"💰 Grand Total: Rs. {bill['grand_total']}")

    # Ask if user wants proper bill when multiple purchases exist
        if filter_date:
            choice = input("Do you want a proper bill for this purchase? (y/n): ").strip().lower()
            if choice == "y":
                print_proper_bill(user_name, bill)

    # If no history matches filter
    if not history_found:
        if filter_date:
            print(f"\n❌ No purchases found for the date {filter_date}")
        else:
            print("\n❌ No purchases found.")

# ===========pyth======= Dashboard Menus ==================
def user_menu(user: dict):
    '''
    User dashboard menu.
    '''
    while True:
        print("\n===== User Dashboard =====")
        print("User Dashboard")
        print("1. View Items")
        print("2. Buy Item")
        print("3. View Purchase History")
        print("4. Update Profile")
        print("5. Logout")
        action = get_valid_action("Enter the action(1-5): ", range(1,6))
        match action:
            case 1:
                view_items()
            case 2:
                buy_item(user['name'], user['email'])
            case 3:
                view_purchase_history(user['name'], user['email'])
            case 4:
                update_profile(user)
            case 5:
                break

def admin_menu(user: dict):
    '''
    Admin dashboard menu.
    Options: Add, View, Update stock, Logout
    '''
    while True:
        print("\n===== Admin Dashboard =====")
        print("Admin Dashboard")
        print("1. Add items")
        print("2. View Stock")
        print("3. Update Stock")
        print("4. Update Profile")
        print("5. logout")
        action = get_valid_action("Enter the action(1-5): ", range(1,6))
        match action:
            case 1:
                add_item()
            case 2:
                view_items()
            case 3:
                update_stock()
            case 4:
                update_profile(user)
            case 5:
                break

# ================== Main Program ==================
def main():
    '''
    Entry point of the program.
    Displays the main menu and routes user based on their choice.
    '''
    while True:
        print("\n===== Grocery Management System =====")
        print("1. Signup")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")

        # Keeps asking until the user provides an integer between 1 and 4
        action = get_valid_action("Enter the action (1-4): ", range(1,5))
        match action:
            case 1:
                signup()
            case 2:
                login()
            case 3:
                login()
            case 4:
                print('Thank you for visiting.')
                sys.exit()

# ================== Entry Point ==================
if __name__ == "__main__":
    main()
