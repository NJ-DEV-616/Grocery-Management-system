# Grocery Management system

#### Description:
The **Grocery Management System** is a Python-based console application designed to manage users, admins, grocery stock, and purchase records. It provides a simple yet functional environment for both customers and administrators. The project uses **JSON files** for persistent data storage, and **tabulate** for formatted outputs.

---

## 📚 Table of Contents


- [📌 Features](#-features)
- [📂 Project Structure](#-project-structure)
- [🛠 Installation & Run](#-installation--run)
- [🚧 Future Improvements](#-future-improvements)
- [🤝 Contributing](#-contributing)
- [🧾 License](#-license)
- [🙏 Final Note](#-final-note)

---

## 📌 Features

### 👤 User Features
- **Signup/Login:** Register or login with email and password validation.
- **View Items:** See all available stock in a formatted table.
- **Buy Items:** Purchase items with bill generation.
- **Purchase History:** View past purchases, optionally filtered by date.
- **Update Profile:** Change name, email, or password.

### 👨‍💼 Admin Features
- **Add Items:** Add new items with count, weight, or volume.
- **Update Stock:** Modify quantity, price, name, or delete items.
- **Undo Last Update:** Revert the most recent stock change.
- **View Stock:** Display current inventory in a formatted table.
- **Update Profile:** Change admin account details.

### 📊 System Features
- **Bill Management:** Logs each purchase with date/time and proper formatting.
- **Persistent Storage:** Uses JSON files (`users.json`, `items.json`, `bills.json`).
- **Input Validation:** Validates menus choice, emails, and passwords.
- **Unit Testing:** Includes tests for validation and input functions.

---
## 📂 Project Structure

- **project.py**: Main program file(entry point)
- **test_project.py**: Unit tests for key function
- **users.json**: Stores registered users
- **items.json**: Stores grocery stock
- **bills.json**: Stores purchase history
- **requirements.txt**: External dependencies
- **README.md**: Project documentation

---

## 🛠 Installation & Run

### Prerequisites
- **Python 3.8+** installed on your system.
- **pip** (Python package manager).
- Python libraries:
  - `tabulate`
  - `pytest` (for running tests, optional)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/NJ-DEV-616/Grocery-Management-system.git
   cd Grocery-Management-system
2. **Install Dependencies**
    ```bash
    pip install tabulate pytest
3. **Run the Program**
    ```bash
    python project.py
4. **Run Unit Tests**
    ```bash
    pytest test_project.py
---

## 🤝 Contributing
1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes
    ```b
    git commit -m "Add feature XYZ"
4. Push your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request — contributions are welcome!

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Final Note
The **Grocery Management System** is a Python console app for managing users, stock, and purchases.
This project can be extended to GUI or web-based systems in the future.

---
