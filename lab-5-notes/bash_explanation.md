### **1. Shebang Line**
```bash
#!/bin/bash
```
- **What it does:** This is called a "shebang" line, and it tells the system that this script should be executed using the Bash shell. Bash is a command interpreter commonly used in Unix-like operating systems such as Linux or macOS.

### **2. Comment Block**
```bash
# CPS510 - Assignment 5
# Application Development with Shell Scripts
# This script provides a menu-driven interface to execute Oracle SQL commands and manage views and tables.
```
- **What it does:** The lines that start with `#` are comments. These comments are not executed by the script; they are just there to provide explanations to anyone reading the code.

### **3. Reading User Input**
```bash
read -p "Enter your Oracle username: " DB_USER
read -sp "Enter your Oracle password: " DB_PASS
echo ""
```
- **What it does:**
  - `read` is a command used to ask the user for input.
  - The `-p` option shows a message asking for the user’s Oracle username, which is then saved in a variable called `DB_USER`.
  - The `-s` option makes the input hidden (for security reasons) when asking for the Oracle password and stores it in the `DB_PASS` variable.
  - `echo ""` adds a new line after entering the password so that it looks nice in the terminal.

### **4. Defining Database Details**
```bash
DB_HOST="oracle12c.cs.torontomu.ca"    # Replace with your Oracle server host
DB_PORT="1521"                          # Default Oracle port
DB_SID="orcl12c"                        # Replace with your Oracle SID
```
- **What it does:** 
  - Three variables are defined here:
    - `DB_HOST`: The server where the Oracle database is hosted.
    - `DB_PORT`: The port number that the Oracle database uses to communicate (the default is `1521`).
    - `DB_SID`: The System Identifier (SID), which uniquely identifies the Oracle database instance you're connecting to.

### **5. Function to Run SQL Files**
```bash
execute_sql_file() {
    sqlplus64 -s "$DB_USER/$DB_PASS@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$DB_HOST)(PORT=$DB_PORT))(CONNECT_DATA=(SID=$DB_SID)))" <<EOF
    @$1
    EXIT;
EOF
}
```
- **What it does:** 
  - This function is called `execute_sql_file`. A function is a reusable block of code that can be run when needed.
  - It uses the `sqlplus64` command, which connects to an Oracle database.
  - It takes the username, password, host, port, and SID, and executes a file that contains SQL statements.
  - The `$1` represents the name of the SQL file passed to the function when it's called. 
  - The function ends with the SQL command `EXIT;` to close the connection after the SQL file is run.

### **6. Function to Execute SQL Queries**
```bash
execute_query() {
    sqlplus64 -s "$DB_USER/$DB_PASS@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$DB_HOST)(PORT=$DB_PORT))(CONNECT_DATA=(SID=$DB_SID)))" <<EOF
SET PAGESIZE 50
SET LINESIZE 150
SET FEEDBACK OFF
SET HEADING ON
$1
EXIT;
EOF
}
```
- **What it does:** 
  - This function, `execute_query`, works similarly to the previous one but is designed to execute an SQL query directly (instead of running a file).
  - The `$1` represents the SQL query string passed into the function when it's called.
  - Before executing the query, it sets some display options (like how many lines of output to show and how wide the output should be).
  - `EXIT;` closes the connection after the query is executed.

### **7. Functions for Managing Tables and Views**
- There are several functions defined for managing tables and views in the Oracle database. Here are some examples:

```bash
create_tables() {
    echo "Running schema creation script..."
    execute_sql_file "schema_creation.sql"
    echo "Tables have been created successfully."
}
```
- **What it does:**
  - `create_tables()` is a function that runs the script `schema_creation.sql` (which contains SQL commands for creating database tables).
  - It uses the `execute_sql_file` function to run this SQL file and then prints a success message.

Other similar functions include:
- `drop_tables()`: Runs a script to drop (delete) all tables.
- `populate_tables()`: Runs a script to insert sample data into the tables.
- `delete_all_data()`: Runs a script to delete all data from the tables.
- `create_views()`: Runs a script to create database views (virtual tables).
- `drop_views()`: Runs a script to drop all views.

### **8. Function to Show the Menu**
```bash
show_menu() {
    echo "----------------------------------------"
    echo " Library Management System - Menu"
    echo "----------------------------------------"
    echo "1. Create Tables (schema creation)"
    echo "2. Drop Tables"
    echo "3. Insert Sample Data"
    echo "4. Delete All Data"
    echo "5. Create Views"
    echo "6. Drop Views"
    echo "7. Find Top 5 Most Borrowed Authors"
    echo "8. List Overdue Loans with Days Overdue"
    echo "9. Find Genres with Most Books"
    echo "10. List Administrators Managing Most Books"
    echo "11. Show Total Fines Collected by Administrators"
    echo "12. Find Authors with No Borrowed Books (EXISTS)"
    echo "13. List All Unique Genres Using UNION"
    echo "14. Show Books Not Borrowed in the Last Year (MINUS)"
    echo "15. Exit"
    echo "----------------------------------------"
    echo -n "Enter your choice [1-15]: "
}
```
- **What it does:**
  - This function prints the main menu of options for the user.
  - The menu offers 15 options, like creating tables, dropping views, finding the most borrowed authors, and so on.
  - `echo` is used to display text, and `echo -n` is used to prompt the user for input without moving to a new line.

### **9. Main Program Loop**
```bash
while true; do
    show_menu
    read choice
    case $choice in
        1)
            clear
            create_tables
            ;;
        2)
            clear
            drop_tables
            ;;
        3)
            clear
            populate_tables
            ;;
        4)
            clear
            delete_all_data
            ;;
        # More cases...
        15)
            echo "Exiting the application. Goodbye!"
            exit 0
            ;;
        *)
            clear
            echo "Invalid option. Please try again."
            ;;
    esac
    echo -n "Press Enter to continue..."
    read
    clear
done
```
- **What it does:**
  - This is the **main loop** of the program. A loop keeps running until a certain condition is met (in this case, until the user chooses to exit by selecting option 15).
  - `show_menu` displays the menu.
  - `read choice` captures the user’s input (their menu choice) and stores it in the `choice` variable.
  - The `case` statement checks what the user entered:
    - If the user enters `1`, it calls the `create_tables()` function to create tables.
    - If the user enters `15`, the program exits by using the `exit 0` command, which means successful termination.
    - If the user enters something invalid, it shows an error message.
  - After each choice, the program waits for the user to press `Enter` and then clears the screen (`clear`) to keep things clean.

### **10. SQL Queries in the Case Statement**
For options like `7`, `8`, etc., SQL queries are embedded in the script using the `execute_query` function. Here’s an example from option 7:
```bash
execute_query "
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
    FETCH FIRST 5 ROWS ONLY;
"
```
- **What it does:** 
  - This SQL query is executed when the user selects option `7` (Find Top 5 Most Borrowed Authors).
  - It selects and counts how many times each author’s books were borrowed and shows the top 5 authors.

---

