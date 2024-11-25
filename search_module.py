# search_module.py

import cx_Oracle
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import box
from rich.panel import Panel

# Initialize Rich Console
console = Console()

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred: {e}[/red]")

# Enhanced Search Records Function with Comparison Operators
def search_records(connection):
    while True:
        search_menu = Panel(
            "\n".join([
                "Search Records",
                "----------------------------------------",
                "1. Search Books",
                "2. Search Authors",
                "3. Search Borrowers",
                "4. Search Users",
                "5. Search Administrators",
                "6. Search Genres",
                "7. Search Loans",              # <--- New Option
                "8. Back to Main Menu",
                "----------------------------------------"
            ]),
            title="Search Menu",
            subtitle="Choose an option [1-8]",
            style="bold cyan",
            box=box.DOUBLE_EDGE
        )
        console.print(search_menu)
        try:
            choice = IntPrompt.ask("Your choice", default=8)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 8.[/red]")
            continue

        console.print("\n")
        if choice == 1:
            search_books(connection)
        elif choice == 2:
            search_authors(connection)
        elif choice == 3:
            search_borrowers(connection)
        elif choice == 4:
            search_users(connection)
        elif choice == 5:
            search_administrators(connection)
        elif choice == 6:
            search_genres(connection)
        elif choice == 7:
            search_loans(connection)       # <--- New Function
        elif choice == 8:
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()

def search_loans(connection):
    console.print("[bold underline]Search Loans[/bold underline]")
    loan_number = Prompt.ask("Enter Loan Number to search (leave blank to skip)")
    borrower_id = Prompt.ask("Enter Borrower ID to search (leave blank to skip)")
    isbn = Prompt.ask("Enter ISBN to search (leave blank to skip)")
    admin_id = Prompt.ask("Enter Admin ID to search (leave blank to skip)")
    return_status = Prompt.ask("Enter Return Status (Y/N) to search (leave blank to skip)", choices=['Y', 'N', ''], default='')
    date_filter = Prompt.ask("Do you want to filter by Loan Date? (y/n)", default='n').lower()
    if date_filter == 'y':
        date_operator = Prompt.ask("Enter operator for Loan Date [>, >=, =, <=, <]")
        date_value = Prompt.ask("Enter Loan Date (YYYY-MM-DD)")
    else:
        date_operator = None
        date_value = None

    query = """
    SELECT
        Loan_Number,
        Borrower_ID,
        ISBN,
        TO_CHAR(Loan_Date, 'YYYY-MM-DD') AS Loan_Date,
        TO_CHAR(Due_Date, 'YYYY-MM-DD') AS Due_Date,
        TO_CHAR(Return_Date, 'YYYY-MM-DD') AS Return_Date,
        Fine_Amount,
        Return_Status,
        Admin_ID
    FROM
        Loans
    WHERE
        1=1
    """
    params = {}
    if loan_number:
        query += " AND Loan_Number = :loan_number"
        params['loan_number'] = loan_number
    if borrower_id:
        query += " AND Borrower_ID = :borrower_id"
        params['borrower_id'] = borrower_id
    if isbn:
        query += " AND ISBN = :isbn"
        params['isbn'] = isbn
    if admin_id:
        query += " AND Admin_ID = :admin_id"
        params['admin_id'] = admin_id
    if return_status:
        query += " AND Return_Status = :return_status"
        params['return_status'] = return_status
    if date_operator and date_value:
        if date_operator not in ['>', '>=', '=', '<=', '<']:
            console.print("[red]Invalid operator for Loan Date. Skipping this filter.[/red]")
        else:
            query += f" AND Loan_Date {date_operator} TO_DATE(:date_value, 'YYYY-MM-DD')"
            params['date_value'] = date_value

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for loans: {e}[/red]")

def search_books(connection):
    console.print("[bold underline]Search Books[/bold underline]")
    isbn = Prompt.ask("Enter ISBN to search (leave blank to skip)")
    title = Prompt.ask("Enter book title to search (leave blank to skip)")
    author = Prompt.ask("Enter author name to search (leave blank to skip)")
    genre = Prompt.ask("Enter genre title to search (leave blank to skip)")

    # Enhanced: Add Publication Date Filters
    pub_date_filter = Prompt.ask("Do you want to filter by Publication Date? (y/n)", default="n").lower()
    if pub_date_filter == 'y':
        pub_date_operator = Prompt.ask("Enter operator for Publication Date [>, >=, =, <=, <]")
        pub_date_value = Prompt.ask("Enter Publication Date (YYYY-MM-DD)")
    else:
        pub_date_operator = None
        pub_date_value = None

    publisher = Prompt.ask("Enter publisher to search (leave blank to skip)")

    query = """
    SELECT
        B.ISBN,
        B.Title,
        A.Name AS Author_Name,
        G.Title AS Genre_Title,
        B.Publication_Date,
        B.Publisher
    FROM
        Books B
    JOIN
        BookAuthor BA ON B.ISBN = BA.ISBN
    JOIN
        Authors A ON BA.Author_ID = A.Author_ID
    JOIN
        BookGenre BG ON B.ISBN = BG.ISBN
    JOIN
        Genres G ON BG.Genre_ID = G.Genre_ID
    WHERE
        1=1
    """
    params = {}
    if isbn:
        query += " AND B.ISBN = :isbn"
        params['isbn'] = isbn
    if title:
        query += " AND LOWER(B.Title) LIKE '%' || LOWER(:title) || '%'"
        params['title'] = title
    if author:
        query += " AND LOWER(A.Name) LIKE '%' || LOWER(:author) || '%'"
        params['author'] = author
    if genre:
        query += " AND LOWER(G.Title) LIKE '%' || LOWER(:genre) || '%'"
        params['genre'] = genre
    if pub_date_operator and pub_date_value:
        if pub_date_operator not in ['>', '>=', '=', '<=', '<']:
            console.print("[red]Invalid operator for Publication Date. Skipping this filter.[/red]")
        else:
            query += f" AND B.Publication_Date {pub_date_operator} TO_DATE(:pub_date_value, 'YYYY-MM-DD')"
            params['pub_date_value'] = pub_date_value
    if publisher:
        query += " AND LOWER(B.Publisher) LIKE '%' || LOWER(:publisher) || '%'"
        params['publisher'] = publisher

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for books: {e}[/red]")

def search_authors(connection):
    console.print("[bold underline]Search Authors[/bold underline]")
    author_id = Prompt.ask("Enter Author ID to search (leave blank to skip)")
    name = Prompt.ask("Enter author name to search (leave blank to skip)")
    nationality = Prompt.ask("Enter nationality to search (leave blank to skip)")

    # Enhanced: Add Date of Birth Filters
    dob_filter = Prompt.ask("Do you want to filter by Date of Birth? (y/n)", default="n").lower()
    if dob_filter == 'y':
        dob_operator = Prompt.ask("Enter operator for Date of Birth [>, >=, =, <=, <]")
        dob_value = Prompt.ask("Enter Date of Birth (YYYY-MM-DD)")
    else:
        dob_operator = None
        dob_value = None

    languages = Prompt.ask("Enter languages to search (leave blank to skip)")

    query = """
    SELECT
        A.Author_ID,
        A.Name,
        A.Nationality,
        A.Date_of_Birth,
        A.Languages
    FROM
        Authors A
    WHERE
        1=1
    """
    params = {}
    if author_id:
        query += " AND A.Author_ID = :author_id"
        params['author_id'] = author_id
    if name:
        query += " AND LOWER(A.Name) LIKE '%' || LOWER(:name) || '%'"
        params['name'] = name
    if nationality:
        query += " AND LOWER(A.Nationality) LIKE '%' || LOWER(:nationality) || '%'"
        params['nationality'] = nationality
    if dob_operator and dob_value:
        if dob_operator not in ['>', '>=', '=', '<=', '<']:
            console.print("[red]Invalid operator for Date of Birth. Skipping this filter.[/red]")
        else:
            query += f" AND A.Date_of_Birth {dob_operator} TO_DATE(:dob_value, 'YYYY-MM-DD')"
            params['dob_value'] = dob_value
    if languages:
        query += " AND LOWER(A.Languages) LIKE '%' || LOWER(:languages) || '%'"
        params['languages'] = languages

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for authors: {e}[/red]")

def search_borrowers(connection):
    console.print("[bold underline]Search Borrowers[/bold underline]")
    borrower_id = Prompt.ask("Enter Borrower ID to search (leave blank to skip)")
    user_name = Prompt.ask("Enter User Name to search (leave blank to skip)")

    # Enhanced: Add Borrowing Limit and Amount Payable Filters
    borrowing_limit_filter = Prompt.ask("Do you want to filter by Borrowing Limit? (y/n)", default="n").lower()
    if borrowing_limit_filter == 'y':
        borrowing_limit_operator = Prompt.ask("Enter operator for Borrowing Limit [>, >=, =, <=, <]")
        borrowing_limit_value = Prompt.ask("Enter Borrowing Limit")
    else:
        borrowing_limit_operator = None
        borrowing_limit_value = None

    amount_payable_filter = Prompt.ask("Do you want to filter by Amount Payable? (y/n)", default="n").lower()
    if amount_payable_filter == 'y':
        amount_payable_operator = Prompt.ask("Enter operator for Amount Payable [>, >=, =, <=, <]")
        amount_payable_value = Prompt.ask("Enter Amount Payable")
    else:
        amount_payable_operator = None
        amount_payable_value = None

    query = """
    SELECT
        BR.Borrower_ID,
        U.First_Name || ' ' || U.Last_Name AS User_Name,
        BR.Borrowing_Limit,
        BR.Amount_Payable
    FROM
        Borrowers BR
    JOIN
        Users U ON BR.User_ID = U.User_ID
    WHERE
        1=1
    """
    params = {}
    if borrower_id:
        query += " AND BR.Borrower_ID = :borrower_id"
        params['borrower_id'] = borrower_id
    if user_name:
        query += " AND LOWER(U.First_Name || ' ' || U.Last_Name) LIKE '%' || LOWER(:user_name) || '%'"
        params['user_name'] = user_name
    if borrowing_limit_operator and borrowing_limit_value:
        if borrowing_limit_operator not in ['>', '>=', '=', '<=', '<']:
            console.print("[red]Invalid operator for Borrowing Limit. Skipping this filter.[/red]")
        else:
            query += f" AND BR.Borrowing_Limit {borrowing_limit_operator} :borrowing_limit_value"
            params['borrowing_limit_value'] = borrowing_limit_value
    if amount_payable_operator and amount_payable_value:
        if amount_payable_operator not in ['>', '>=', '=', '<=', '<']:
            console.print("[red]Invalid operator for Amount Payable. Skipping this filter.[/red]")
        else:
            query += f" AND BR.Amount_Payable {amount_payable_operator} :amount_payable_value"
            params['amount_payable_value'] = amount_payable_value

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for borrowers: {e}[/red]")

def search_users(connection):
    console.print("[bold underline]Search Users[/bold underline]")
    user_id = Prompt.ask("Enter User ID to search (leave blank to skip)")
    first_name = Prompt.ask("Enter First Name to search (leave blank to skip)")
    last_name = Prompt.ask("Enter Last Name to search (leave blank to skip)")
    phone_number = Prompt.ask("Enter Phone Number to search (leave blank to skip)")
    email = Prompt.ask("Enter Email to search (leave blank to skip)")
    username = Prompt.ask("Enter Username to search (leave blank to skip)")
    street = Prompt.ask("Enter Street to search (leave blank to skip)")
    city = Prompt.ask("Enter City to search (leave blank to skip)")
    state = Prompt.ask("Enter State to search (leave blank to skip)")
    zip_code = Prompt.ask("Enter ZIP Code to search (leave blank to skip)")

    # Enhanced: Add ZIP Code Comparison (if needed)
    zip_code_filter = Prompt.ask("Do you want to apply a specific condition on ZIP Code? (y/n)", default="n").lower()
    if zip_code_filter == 'y':
        zip_operator = Prompt.ask("Enter operator for ZIP Code [=]")
        zip_value = Prompt.ask("Enter ZIP Code")
    else:
        zip_operator = None
        zip_value = None

    query = """
    SELECT
        U.User_ID,
        U.First_Name,
        U.Last_Name,
        U.Phone_Number,
        U.Email,
        U.Username,
        U.Street,
        U.City,
        U.State,
        U.ZIP_Code
    FROM
        Users U
    WHERE
        1=1
    """
    params = {}
    if user_id:
        query += " AND U.User_ID = :user_id"
        params['user_id'] = user_id
    if first_name:
        query += " AND LOWER(U.First_Name) LIKE '%' || LOWER(:first_name) || '%'"
        params['first_name'] = first_name
    if last_name:
        query += " AND LOWER(U.Last_Name) LIKE '%' || LOWER(:last_name) || '%'"
        params['last_name'] = last_name
    if phone_number:
        query += " AND U.Phone_Number = :phone_number"
        params['phone_number'] = phone_number
    if email:
        query += " AND LOWER(U.Email) LIKE '%' || LOWER(:email) || '%'"
        params['email'] = email
    if username:
        query += " AND LOWER(U.Username) LIKE '%' || LOWER(:username) || '%'"
        params['username'] = username
    if street:
        query += " AND LOWER(U.Street) LIKE '%' || LOWER(:street) || '%'"
        params['street'] = street
    if city:
        query += " AND LOWER(U.City) LIKE '%' || LOWER(:city) || '%'"
        params['city'] = city
    if state:
        query += " AND LOWER(U.State) LIKE '%' || LOWER(:state) || '%'"
        params['state'] = state
    if zip_operator and zip_value:
        if zip_operator != '=':
            console.print("[red]Invalid operator for ZIP Code. Only '=' is allowed.[/red]")
        else:
            query += " AND U.ZIP_Code = :zip_code"
            params['zip_code'] = zip_value

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for users: {e}[/red]")

def search_administrators(connection):
    console.print("[bold underline]Search Administrators[/bold underline]")
    admin_id = Prompt.ask("Enter Admin ID to search (leave blank to skip)")
    user_name = Prompt.ask("Enter User Name to search (leave blank to skip)")
    role = Prompt.ask("Enter Role to search (leave blank to skip)")
    permissions = Prompt.ask("Enter Permissions to search (leave blank to skip)")

    query = """
    SELECT
        A.Admin_ID,
        U.First_Name || ' ' || U.Last_Name AS User_Name,
        A.Role,
        A.Permissions,
        A.Last_Login
    FROM
        Administrators A
    JOIN
        Users U ON A.User_ID = U.User_ID
    WHERE
        1=1
    """
    params = {}
    if admin_id:
        query += " AND A.Admin_ID = :admin_id"
        params['admin_id'] = admin_id
    if user_name:
        query += " AND LOWER(U.First_Name || ' ' || U.Last_Name) LIKE '%' || LOWER(:user_name) || '%'"
        params['user_name'] = user_name
    if role:
        query += " AND LOWER(A.Role) LIKE '%' || LOWER(:role) || '%'"
        params['role'] = role
    if permissions:
        query += " AND LOWER(A.Permissions) LIKE '%' || LOWER(:permissions) || '%'"
        params['permissions'] = permissions

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for administrators: {e}[/red]")

def search_genres(connection):
    console.print("[bold underline]Search Genres[/bold underline]")
    genre_id = Prompt.ask("Enter Genre ID to search (leave blank to skip)")
    title = Prompt.ask("Enter Genre Title to search (leave blank to skip)")
    description = Prompt.ask("Enter Description to search (leave blank to skip)")

    query = """
    SELECT
        G.Genre_ID,
        G.Title,
        G.Description
    FROM
        Genres G
    WHERE
        1=1
    """
    params = {}
    if genre_id:
        query += " AND G.Genre_ID = :genre_id"
        params['genre_id'] = genre_id
    if title:
        query += " AND LOWER(G.Title) LIKE '%' || LOWER(:title) || '%'"
        params['title'] = title
    if description:
        query += " AND LOWER(G.Description) LIKE '%' || LOWER(:description) || '%'"
        params['description'] = description

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
    except cx_Oracle.DatabaseError as e:
        console.print(f"[red]An error occurred while searching for genres: {e}[/red]")

# Function to display messages between operations
def pause():
    console.print("\nPress [bold cyan]Enter[/bold cyan] to continue...")
    input()
