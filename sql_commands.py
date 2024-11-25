#!/usr/bin/env python3

import cx_Oracle
import getpass
import sys
import os
import re
import validators
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich import box

# Import the search module for option 15
import search_module  # <--- New Import
import ra_module

# Initialize Rich Console
console = Console()

# Database connection parameters
DB_HOST = "oracle12c.cs.torontomu.ca"  # Replace with your Oracle server host
DB_PORT = 1521                          # Default Oracle port
DB_SID = "orcl12c"                      # Replace with your Oracle SID

# Function to establish database connection
def get_db_connection(username, password):
    dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, sid=DB_SID)
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        return connection
    except cx_Oracle.DatabaseError as e:
        # Suppress detailed error messages for silent operations
        if username and password:
            # Attempt to provide minimal feedback if credentials are provided
            console.print("[red]Failed to connect to the Oracle database. Please check your credentials and try again.[/red]")
        sys.exit(1)

# Function to clean and split SQL script into executable statements
def split_sql_statements(sql_script):
    # Remove all block comments (/* */)
    sql_script = re.sub(r'/\*.*?\*/', '', sql_script, flags=re.DOTALL)
    # Remove all single-line comments (-- ...)
    sql_script = re.sub(r'--.*', '', sql_script)
    # Split by semicolon
    statements = sql_script.strip().split(';')
    # Remove any leading/trailing whitespace from each statement
    statements = [stmt.strip() for stmt in statements]
    return statements

# Function to execute SQL from a file without printing errors
def execute_sql_file(connection, file_path):
    if not os.path.isfile(file_path):
        return False

    with open(file_path, 'r') as file:
        sql_script = file.read()

    statements = split_sql_statements(sql_script)

    try:
        cursor = connection.cursor()
        for stmt in statements:
            if not stmt:
                continue
            if stmt.upper().startswith('SET') or stmt.upper().startswith('SPOOL'):
                continue
            try:
                cursor.execute(stmt)
            except cx_Oracle.DatabaseError:
                continue  # Silently ignore errors
        connection.commit()
        cursor.close()
        return True
    except cx_Oracle.DatabaseError:
        try:
            connection.rollback()
        except:
            pass
        return False

# Function to run SQL scripts silently for options 1-6
def silent_execute(connection, file_path):
    execute_sql_file(connection, file_path)
    console.print("Finished executing script.")

# Functions corresponding to menu options 1-6
def create_tables(connection):
    silent_execute(connection, "schema_creation.sql")

def drop_tables(connection):
    silent_execute(connection, "delete_all_tables.sql")

def populate_tables(connection):
    silent_execute(connection, "insert_sample_data.sql")

def delete_all_data(connection):
    silent_execute(connection, "delete_all_data.sql")

def create_views(connection):
    silent_execute(connection, "create_views.sql")

def drop_views(connection):
    silent_execute(connection, "delete_all_views.sql")

# Function to execute an inline SQL query and display results
def execute_query(connection, query, params=None):
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL_DOUBLE_HEAD)
        for col in columns:
            table.add_column(str(col))
        for row in cursor:
            table.add_row(*[str(item) if item is not None else "NULL" for item in row])
        console.print(table)
        cursor.close()
    except cx_Oracle.DatabaseError:
        pass  # Silently ignore query execution errors

def find_top_borrowed_authors(connection):
    query = """
    SELECT
        A.Author_ID,
        A.Name AS Author_Name,
        COUNT(L.Loan_Number) AS Borrow_Count
    FROM
        Authors A
    JOIN
        BookAuthor BA ON A.Author_ID = BA.Author_ID
    JOIN
        Loans L ON BA.ISBN = L.ISBN
    GROUP BY
        A.Author_ID, A.Name
    ORDER BY
        Borrow_Count DESC
    FETCH FIRST 5 ROWS ONLY
    """
    execute_query(connection, query)

def list_overdue_loans(connection):
    query = """
    SELECT
        BR.Borrower_ID,
        U.First_Name || ' ' || U.Last_Name AS Borrower_Name,
        L.Loan_Number,
        L.Due_Date,
        L.Return_Status,
        TRUNC(SYSDATE - L.Due_Date) AS Days_Overdue
    FROM
        Loans L
    JOIN
        Borrowers BR ON L.Borrower_ID = BR.Borrower_ID
    JOIN
        Users U ON BR.User_ID = U.User_ID
    WHERE
        L.Return_Status = 'N'
        AND L.Due_Date < SYSDATE
    ORDER BY
        Days_Overdue DESC
    """
    execute_query(connection, query)

def find_genres_with_most_books(connection):
    query = """
    SELECT
        G.Genre_ID,
        G.Title AS Genre_Title,
        COUNT(BG.ISBN) AS Number_of_Books
    FROM
        Genres G
    JOIN
        BookGenre BG ON G.Genre_ID = BG.Genre_ID
    GROUP BY
        G.Genre_ID, G.Title
    HAVING COUNT(BG.ISBN) > 1
    """
    execute_query(connection, query)

def list_admins_managing_most_books(connection):
    query = """
    SELECT
        A.Admin_ID,
        U.First_Name || ' ' || U.Last_Name AS Admin_Name,
        COUNT(B.ISBN) AS Books_Managed
    FROM
        Administrators A
    JOIN
        Users U ON A.User_ID = U.User_ID
    JOIN
        Books B ON A.Admin_ID = B.Admin_ID
    GROUP BY
        A.Admin_ID, U.First_Name, U.Last_Name
    ORDER BY
        Books_Managed DESC
    """
    execute_query(connection, query)

def show_total_fines(connection):
    query = """
    SELECT
        A.Admin_ID,
        U.First_Name || ' ' || U.Last_Name AS Admin_Name,
        SUM(L.Fine_Amount) AS Total_Fines_Collected
    FROM
        Administrators A
    JOIN
        Users U ON A.User_ID = U.User_ID
    JOIN
        Loans L ON A.Admin_ID = L.Admin_ID
    GROUP BY
        A.Admin_ID, U.First_Name, U.Last_Name
    ORDER BY
        Total_Fines_Collected DESC
    """
    execute_query(connection, query)

def find_authors_no_borrowed_books(connection):
    query = """
    SELECT
        A.Author_ID,
        A.Name AS Author_Name
    FROM
        Authors A
    WHERE
        NOT EXISTS (
            SELECT 1
            FROM BookAuthor BA
            JOIN Loans L ON BA.ISBN = L.ISBN
            WHERE BA.Author_ID = A.Author_ID
        )
    """
    execute_query(connection, query)

def list_unique_genres(connection):
    query = """
    SELECT Title AS Genre_Title FROM Genres
    UNION
    SELECT DISTINCT G.Title AS Genre_Title FROM Genres G
    """
    execute_query(connection, query)

def show_books_not_borrowed_last_year(connection):
    query = """
    SELECT
        B.ISBN,
        B.Title
    FROM
        Books B
    WHERE
        B.ISBN NOT IN (
            SELECT L.ISBN
            FROM Loans L
            WHERE L.Loan_Date >= ADD_MONTHS(SYSDATE, -12)
        )
    """
    execute_query(connection, query)

# New Functions: Adding, Updating, Deleting Records

def add_record(connection):
    while True:
        add_menu = Panel(
            "\n".join([
                "Add Records",
                "----------------------------------------",
                "1. Add Book",
                "2. Add Author",
                "3. Add Borrower",
                "4. Add User",
                "5. Add Administrator",
                "6. Add Genre",
                "7. Add Loan",             # <--- New Option
                "8. Back to Main Menu",
                "----------------------------------------"
            ]),
            title="Add Menu",
            subtitle="Choose an option [1-8]",
            style="bold green",
            box=box.DOUBLE_EDGE
        )
        console.print(add_menu)
        try:
            choice = IntPrompt.ask("Your choice", default=8)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 8.[/red]")
            continue

        console.print("\n")
        if choice == 1:
            add_book(connection)
        elif choice == 2:
            add_author(connection)
        elif choice == 3:
            add_borrower(connection)
        elif choice == 4:
            add_user(connection)
        elif choice == 5:
            add_administrator(connection)
        elif choice == 6:
            add_genre(connection)
        elif choice == 7:
            add_loan(connection)       # <--- New Function
        elif choice == 8:
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()

def add_user(connection, user_id=None):
    console.print("[bold underline]Add New User[/bold underline]")
    if user_id is None:
        user_id = Prompt.ask("Enter User ID")

    # Check if User ID already exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE User_ID = :user_id", user_id=user_id)
    if cursor.fetchone() is not None:
        console.print(f"[red]User ID {user_id} already exists. Please use a different User ID.[/red]")
        cursor.close()
        return
    cursor.close()

    first_name = Prompt.ask("Enter First Name")
    last_name = Prompt.ask("Enter Last Name")
    phone_number = Prompt.ask("Enter Phone Number")
    email = Prompt.ask("Enter Email")
    while not validators.email(email):
        console.print("[red]Invalid email format. Please enter a valid email address.[/red]")
        email = Prompt.ask("Enter Email")

    username = Prompt.ask("Enter Username")
    password = Prompt.ask("Enter Password")
    street = Prompt.ask("Enter Street")
    city = Prompt.ask("Enter City")
    state = Prompt.ask("Enter State")
    zip_code = Prompt.ask("Enter ZIP Code")
    while not validate_zip_code(zip_code):
        console.print("[red]Invalid ZIP Code format. Please enter a valid US or Canadian ZIP Code.[/red]")
        zip_code = Prompt.ask("Enter ZIP Code")

    query = """
    INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code)
    VALUES (:user_id, :first_name, :last_name, :phone_number, :email, :username, :password, :street, :city, :state, :zip_code)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, user_id=user_id, first_name=first_name, last_name=last_name,
                       phone_number=phone_number, email=email, username=username, password=password,
                       street=street, city=city, state=state, zip_code=zip_code)
        connection.commit()
        console.print("[green]User added successfully.[/green]")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Failed to add user: {error.message}[/red]")

def validate_zip_code(zip_code):
    us_zip_pattern = r'^\d{5}(?:-\d{4})?$'
    ca_zip_pattern = r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$'
    return re.match(us_zip_pattern, zip_code) or re.match(ca_zip_pattern, zip_code)

def update_administrator(connection):
    console.print("[bold underline]Update Administrator[/bold underline]")
    admin_id = Prompt.ask("Enter Admin ID to update")

    # Fetch current data
    query = "SELECT User_ID, Role, Permissions, Last_Login FROM Administrators WHERE Admin_ID = :admin_id"
    try:
        cursor = connection.cursor()
        cursor.execute(query, admin_id=admin_id)
        result = cursor.fetchone()
        if not result:
            console.print("[red]Administrator not found.[/red]")
            cursor.close()
            return
        current_user_id, current_role, current_permissions, current_last_login = result
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Error fetching administrator: {error.message}[/red]")
        return

    # Prompt for new data
    user_id = Prompt.ask(f"Enter new User ID (current: {current_user_id})", default=str(current_user_id))

    # Check if User ID exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE User_ID = :user_id", user_id=user_id)
    if cursor.fetchone() is None:
        console.print(f"[red]User ID {user_id} does not exist. Please add the user first.[/red]")
        cursor.close()
        return
    cursor.close()

    role = Prompt.ask(f"Enter new Role (current: {current_role})", default=current_role)
    while not validate_role(role):
        console.print("[red]Invalid role format. Role should be 'Admin', 'Librarian', or 'Manager'.[/red]")
        role = Prompt.ask("Enter Role")

    permissions = Prompt.ask(f"Enter new Permissions (current: {current_permissions})", default=current_permissions)
    while not validate_permissions(permissions):
        console.print("[red]Invalid permissions format. Permissions should be a comma-separated list of permissions.[/red]")
        permissions = Prompt.ask("Enter Permissions")

    last_login = Prompt.ask(f"Enter new Last Login Date (YYYY-MM-DD) (current: {current_last_login.strftime('%Y-%m-%d') if current_last_login else 'N/A'})",
                            default=current_last_login.strftime('%Y-%m-%d') if current_last_login else None)

    update_query = """
    UPDATE Administrators
    SET User_ID = :user_id,
        Role = :role,
        Permissions = :permissions,
        Last_Login = TO_DATE(:last_login, 'YYYY-MM-DD')
    WHERE Admin_ID = :admin_id
    """
    try:
        cursor = connection.cursor()
        cursor.execute(update_query, user_id=user_id, role=role, permissions=permissions,
                       last_login=last_login if last_login else None, admin_id=admin_id)
        connection.commit()
        console.print("[green]Administrator updated successfully.[/green]")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Failed to update administrator: {error.message}[/red]")

def validate_role(role):
    valid_roles = ['Admin', 'Librarian', 'Manager']
    return role in valid_roles

def validate_permissions(permissions):
    # Permissions should be a comma-separated list of alphanumeric permissions
    return all(re.match(r'^\w+$', perm.strip()) for perm in permissions.split(','))

def add_loan(connection):
    console.print("[bold underline]Add New Loan[/bold underline]")
    loan_number = Prompt.ask("Enter Loan Number")
    # Check if Loan Number already exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Loans WHERE Loan_Number = :loan_number", loan_number=loan_number)
    if cursor.fetchone():
        console.print(f"[red]Loan Number {loan_number} already exists. Please use a different Loan Number.[/red]")
        cursor.close()
        return
    cursor.close()

    borrower_id = Prompt.ask("Enter Borrower ID")
    # Check if Borrower ID exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Borrowers WHERE Borrower_ID = :borrower_id", borrower_id=borrower_id)
    if cursor.fetchone() is None:
        console.print(f"[red]Borrower ID {borrower_id} does not exist.[/red]")
        cursor.close()
        return
    cursor.close()

    isbn = Prompt.ask("Enter ISBN")
    # Check if ISBN exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Books WHERE ISBN = :isbn", isbn=isbn)
    if cursor.fetchone() is None:
        console.print(f"[red]ISBN {isbn} does not exist.[/red]")
        cursor.close()
        return
    cursor.close()

    admin_id = Prompt.ask("Enter Admin ID")
    # Check if Admin ID exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Administrators WHERE Admin_ID = :admin_id", admin_id=admin_id)
    if cursor.fetchone() is None:
        console.print(f"[red]Admin ID {admin_id} does not exist.[/red]")
        cursor.close()
        return
    cursor.close()

    loan_date = Prompt.ask("Enter Loan Date (YYYY-MM-DD)", default=None)
    due_date = Prompt.ask("Enter Due Date (YYYY-MM-DD)")
    return_status = Prompt.ask("Enter Return Status (Y/N)", choices=['Y', 'N'], default='N')

    # Validate dates
    if not due_date:
        console.print("[red]Due Date is required.[/red]")
        return

    if loan_date:
        if not validate_date_format(loan_date):
            console.print("[red]Invalid Loan Date format.[/red]")
            return
    else:
        loan_date = None

    if not validate_date_format(due_date):
        console.print("[red]Invalid Due Date format.[/red]")
        return

    if loan_date and not validate_date_order(loan_date, due_date):
        console.print("[red]Due Date cannot be earlier than Loan Date.[/red]")
        return

    query = """
    INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID)
    VALUES (:loan_number, :borrower_id, :isbn, TO_DATE(:loan_date, 'YYYY-MM-DD'), TO_DATE(:due_date, 'YYYY-MM-DD'), :return_status, :admin_id)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, loan_number=loan_number, borrower_id=borrower_id, isbn=isbn,
                       loan_date=loan_date, due_date=due_date, return_status=return_status, admin_id=admin_id)
        connection.commit()
        console.print("[green]Loan added successfully.[/green]")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Failed to add loan: {error.message}[/red]")

def validate_date_format(date_text):
    try:
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_text))
    except ValueError:
        return False

def validate_date_order(start_date, end_date):
    from datetime import datetime
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return end >= start

def update_record(connection):
    while True:
        update_menu = Panel(
            "\n".join([
                "Update Records",
                "----------------------------------------",
                "1. Update Book",
                "2. Update Author",
                "3. Update Borrower",
                "4. Update User",
                "5. Update Administrator",
                "6. Update Book Genres",
                "7. Update Book Authors",
                "8. Update Genre",
                "9. Update Loan",                 # <--- New Option
                "10. Back to Main Menu",
                "----------------------------------------"
            ]),
            title="Update Menu",
            subtitle="Choose an option [1-10]",
            style="bold yellow",
            box=box.DOUBLE_EDGE
        )
        console.print(update_menu)
        try:
            choice = IntPrompt.ask("Your choice", default=10)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 10.[/red]")
            continue

        console.print("\n")
        if choice == 1:
            update_book(connection)
        elif choice == 2:
            update_author(connection)
        elif choice == 3:
            update_borrower(connection)
        elif choice == 4:
            update_user(connection)
        elif choice == 5:
            update_administrator(connection)
        elif choice == 6:
            manage_book_genres(connection)
        elif choice == 7:
            manage_book_authors(connection)
        elif choice == 8:
            update_genre(connection)
        elif choice == 9:
            update_loan(connection)           # <--- New Function
        elif choice == 10:
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()

def update_loan(connection):
    console.print("[bold underline]Update Loan[/bold underline]")
    loan_number = Prompt.ask("Enter Loan Number to update")

    # Fetch current data
    query = "SELECT Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Date, Fine_Amount, Return_Status, Admin_ID FROM Loans WHERE Loan_Number = :loan_number"
    try:
        cursor = connection.cursor()
        cursor.execute(query, loan_number=loan_number)
        result = cursor.fetchone()
        if not result:
            console.print("[red]Loan not found.[/red]")
            cursor.close()
            return
        (current_borrower_id, current_isbn, current_loan_date, current_due_date, current_return_date,
         current_fine_amount, current_return_status, current_admin_id) = result
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Error fetching loan: {error.message}[/red]")
        return

    # Prompt for new data
    borrower_id = Prompt.ask(f"Enter new Borrower ID (current: {current_borrower_id})", default=str(current_borrower_id))
    # Check if Borrower ID exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Borrowers WHERE Borrower_ID = :borrower_id", borrower_id=borrower_id)
    if cursor.fetchone() is None:
        console.print(f"[red]Borrower ID {borrower_id} does not exist.[/red]")
        cursor.close()
        return
    cursor.close()

    isbn = Prompt.ask(f"Enter new ISBN (current: {current_isbn})", default=current_isbn)
    # Check if ISBN exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Books WHERE ISBN = :isbn", isbn=isbn)
    if cursor.fetchone() is None:
        console.print(f"[red]ISBN {isbn} does not exist.[/red]")
        cursor.close()
        return
    cursor.close()

    loan_date = Prompt.ask(f"Enter new Loan Date (YYYY-MM-DD) (current: {current_loan_date.strftime('%Y-%m-%d') if current_loan_date else 'N/A'})",
                           default=current_loan_date.strftime('%Y-%m-%d') if current_loan_date else None)
    due_date = Prompt.ask(f"Enter new Due Date (YYYY-MM-DD) (current: {current_due_date.strftime('%Y-%m-%d') if current_due_date else 'N/A'})",
                          default=current_due_date.strftime('%Y-%m-%d') if current_due_date else None)
    return_date = Prompt.ask(f"Enter new Return Date (YYYY-MM-DD) (current: {current_return_date.strftime('%Y-%m-%d') if current_return_date else 'N/A'})",
                             default=current_return_date.strftime('%Y-%m-%d') if current_return_date else None)
    fine_amount = Prompt.ask(f"Enter new Fine Amount (current: {current_fine_amount})", default=str(current_fine_amount))
    return_status = Prompt.ask(f"Enter new Return Status (Y/N) (current: {current_return_status})",
                               choices=['Y', 'N'], default=current_return_status)
    admin_id = Prompt.ask(f"Enter new Admin ID (current: {current_admin_id})", default=str(current_admin_id))
    # Check if Admin ID exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Administrators WHERE Admin_ID = :admin_id", admin_id=admin_id)
    if cursor.fetchone() is None:
        console.print(f"[red]Admin ID {admin_id} does not exist.[/red]")
        cursor.close()
        return
    cursor.close()

    # Validate dates
    if loan_date and not validate_date_format(loan_date):
        console.print("[red]Invalid Loan Date format.[/red]")
        return
    if due_date and not validate_date_format(due_date):
        console.print("[red]Invalid Due Date format.[/red]")
        return
    if return_date and not validate_date_format(return_date):
        console.print("[red]Invalid Return Date format.[/red]")
        return
    if loan_date and due_date and not validate_date_order(loan_date, due_date):
        console.print("[red]Due Date cannot be earlier than Loan Date.[/red]")
        return
    if loan_date and return_date and not validate_date_order(loan_date, return_date):
        console.print("[red]Return Date cannot be earlier than Loan Date.[/red]")
        return

    update_query = """
    UPDATE Loans
    SET Borrower_ID = :borrower_id,
        ISBN = :isbn,
        Loan_Date = TO_DATE(:loan_date, 'YYYY-MM-DD'),
        Due_Date = TO_DATE(:due_date, 'YYYY-MM-DD'),
        Return_Date = TO_DATE(:return_date, 'YYYY-MM-DD'),
        Fine_Amount = :fine_amount,
        Return_Status = :return_status,
        Admin_ID = :admin_id
    WHERE Loan_Number = :loan_number
    """
    try:
        cursor = connection.cursor()
        cursor.execute(update_query, borrower_id=borrower_id, isbn=isbn,
                       loan_date=loan_date if loan_date else None,
                       due_date=due_date if due_date else None,
                       return_date=return_date if return_date else None,
                       fine_amount=fine_amount, return_status=return_status,
                       admin_id=admin_id, loan_number=loan_number)
        connection.commit()
        console.print("[green]Loan updated successfully.[/green]")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Failed to update loan: {error.message}[/red]")

def delete_record(connection):
    while True:
        delete_menu = Panel(
            "\n".join([
                "Delete Records",
                "----------------------------------------",
                "1. Delete Book",
                "2. Delete Author",
                "3. Delete Borrower",
                "4. Delete User",
                "5. Delete Administrator",
                "6. Delete Genre",
                "7. Delete Loan",            # <--- New Option
                "8. Back to Main Menu",
                "----------------------------------------"
            ]),
            title="Delete Menu",
            subtitle="Choose an option [1-8]",
            style="bold red",
            box=box.DOUBLE_EDGE
        )
        console.print(delete_menu)
        try:
            choice = IntPrompt.ask("Your choice", default=8)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 8.[/red]")
            continue

        console.print("\n")
        if choice == 1:
            delete_book(connection)
        elif choice == 2:
            delete_author(connection)
        elif choice == 3:
            delete_borrower(connection)
        elif choice == 4:
            delete_user(connection)
        elif choice == 5:
            delete_administrator(connection)
        elif choice == 6:
            delete_genre(connection)
        elif choice == 7:
            delete_loan(connection)     # <--- New Function
        elif choice == 8:
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()

def delete_loan(connection):
    console.print("[bold underline]Delete Loan[/bold underline]")
    loan_number = Prompt.ask("Enter Loan Number to delete")

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Loans WHERE Loan_Number = :loan_number", loan_number=loan_number)
        if cursor.rowcount == 0:
            console.print("[red]No loan found with the provided Loan Number.[/red]")
        else:
            connection.commit()
            console.print("[green]Loan deleted successfully.[/green]")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]Failed to delete loan: {error.message}[/red]")

# Function to display messages between operations
def pause():
    console.print("\nPress [bold cyan]Enter[/bold cyan] to continue...")
    input()

# Function to display the menu
def show_menu():
    menu = Panel(
        "\n".join([
            "Library Management System - Menu",
            "----------------------------------------",
            "1. Create Tables (schema creation)",
            "2. Drop Tables",
            "3. Insert Sample Data",
            "4. Delete All Data",
            "5. Create Views",
            "6. Drop Views",
            "7. Find Top 5 Most Borrowed Authors",
            "8. List Overdue Loans with Days Overdue",
            "9. Find Genres with Most Books",
            "10. List Administrators Managing Most Books",
            "11. Show Total Fines Collected by Administrators",
            "12. Find Authors with No Borrowed Books (EXISTS)",
            "13. List All Unique Genres Using UNION",
            "14. Show Books Not Borrowed in the Last Year",
            "15. Search for Records",
            "16. Add Records",
            "17. Update Records",
            "18. Delete Records",
            "19. Relational Algebra",
            "20. Exit",
            "----------------------------------------"
        ]),
        title="Main Menu",
        subtitle="Enter your choice [1-20]",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(menu)

# Main function
def main():
    console.print(Panel("Welcome to the Library Management System", style="bold green"))

    # Prompt for database credentials
    DB_USER = Prompt.ask("Enter your Oracle username")
    DB_PASS = getpass.getpass("Enter your Oracle password: ")

    # Establish database connection
    connection = get_db_connection(DB_USER, DB_PASS)

    while True:
        show_menu()
        try:
            choice = IntPrompt.ask("Your choice", default=20)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 20.[/red]")
            continue

        console.print("\n")
        if choice == 1:
            create_tables(connection)
        elif choice == 2:
            drop_tables(connection)
        elif choice == 3:
            populate_tables(connection)
        elif choice == 4:
            delete_all_data(connection)
        elif choice == 5:
            create_views(connection)
        elif choice == 6:
            drop_views(connection)
        elif choice == 7:
            find_top_borrowed_authors(connection)
        elif choice == 8:
            list_overdue_loans(connection)
        elif choice == 9:
            find_genres_with_most_books(connection)
        elif choice == 10:
            list_admins_managing_most_books(connection)
        elif choice == 11:
            show_total_fines(connection)
        elif choice == 12:
            find_authors_no_borrowed_books(connection)
        elif choice == 13:
            list_unique_genres(connection)
        elif choice == 14:
            show_books_not_borrowed_last_year(connection)
        elif choice == 15:
            search_module.search_records(connection)  # <--- Modified to use imported module
        elif choice == 16:
            add_record(connection)
        elif choice == 17:
            update_record(connection)
        elif choice == 18:
            delete_record(connection)
        elif choice == 19:
            ra_module.ra_operations(connection)
        elif choice == 20:
            console.print("[bold magenta]Exiting the application. Goodbye![/bold magenta]")
            connection.close()
            sys.exit(0)
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()
        console.clear()

if __name__ == "__main__":
    main()