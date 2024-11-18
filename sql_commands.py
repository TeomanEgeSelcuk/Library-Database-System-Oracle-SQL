#!/usr/bin/env python3

import cx_Oracle
import getpass
import sys
import os
import re
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich import box

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
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
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

# Queries for options 7 to 14
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
            "15. Exit",
            "----------------------------------------"
        ]),
        title="Main Menu",
        subtitle="Enter your choice [1-15]",
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
            choice = IntPrompt.ask("Your choice", default=15)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 15.[/red]")
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
            console.print("[bold magenta]Exiting the application. Goodbye![/bold magenta]")
            connection.close()
            sys.exit(0)
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()
        console.clear()

if __name__ == "__main__":
    main()
