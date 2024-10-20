#!/bin/bash

# CPS510 - Assignment 5
# Application Development with Shell Scripts
# This script provides a menu-driven interface to execute Oracle SQL commands and manage views and tables.

# Prompt the user for database credentials
read -p "Enter your Oracle username: " DB_USER
read -sp "Enter your Oracle password: " DB_PASS
echo ""
DB_HOST="oracle12c.cs.torontomu.ca"    # Replace with your Oracle server host
DB_PORT="1521"                          # Default Oracle port
DB_SID="orcl12c"                        # Replace with your Oracle SID

# Function to execute an SQL file using sqlplus
execute_sql_file() {
    sqlplus64 -s "$DB_USER/$DB_PASS@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=$DB_HOST)(PORT=$DB_PORT))(CONNECT_DATA=(SID=$DB_SID)))" <<EOF
    @$1
    EXIT;
EOF
}

# Function to execute SQL queries using sqlplus
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

# Function to create tables (schema creation)
create_tables() {
    echo "Running schema creation script..."
    execute_sql_file "schema_creation.sql"
    echo "Tables have been created successfully."
}

# Function to drop tables
drop_tables() {
    echo "Running delete all tables script..."
    execute_sql_file "delete_all_tables.sql"
    echo "Tables have been dropped successfully."
}

# Function to insert sample data
populate_tables() {
    echo "Running insert sample data script..."
    execute_sql_file "insert_sample_data.sql"
    echo "Sample data has been inserted successfully."
}

# Function to delete all data
delete_all_data() {
    echo "Running delete all data script..."
    execute_sql_file "delete_all_data.sql"
    echo "All data has been deleted successfully."
}

# Function to create views
create_views() {
    echo "Running create views script..."
    execute_sql_file "create_views.sql"
    echo "Views have been created successfully."
}

# Function to drop views
drop_views() {
    echo "Running delete all views script..."
    execute_sql_file "delete_all_views.sql"
    echo "Views have been dropped successfully."
}

# Menu display function
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

# Main loop to display menu and execute chosen option
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
        5)
            clear
            create_views
            ;;
        6)
            clear
            drop_views
            ;;
        7)
            clear
            echo "Top 5 Most Borrowed Authors:"
            echo "----------------------------------------"
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
            echo "----------------------------------------"
            ;;
        8)
            clear
            echo "Borrowers with Overdue Loans:"
            echo "----------------------------------------"
            execute_query "
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
        Days_Overdue DESC;
    "
            echo "----------------------------------------"
            ;;
        9)
            clear
            echo "Genres with Most Books:"
            echo "----------------------------------------"
            execute_query "
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
    HAVING COUNT(BG.ISBN) > 1;  -- Genres with more than 1 book
    "
            echo "----------------------------------------"
            ;;
        10)
            clear
            echo "Administrators Managing Most Books:"
            echo "----------------------------------------"
            execute_query "
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
        Books_Managed DESC;
    "
            echo "----------------------------------------"
            ;;
        11)
            clear
            echo "Total Fines Collected by Administrators:"
            echo "----------------------------------------"
            execute_query "
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
        Total_Fines_Collected DESC;
    "
            echo "----------------------------------------"
            ;;
        12)
            clear
            echo "Authors with No Borrowed Books:"
            echo "----------------------------------------"
            execute_query "
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
        );
    "
            echo "----------------------------------------"
            ;;
        13)
            clear
            echo "All Unique Genres:"
            echo "----------------------------------------"
            execute_query "
    SELECT Genre_Title FROM Genres
    UNION
    SELECT DISTINCT G.Title FROM Genres G;
    "
            echo "----------------------------------------"
            ;;
        14)
            clear
            echo "Books Not Borrowed in the Last Year:"
            echo "----------------------------------------"
            execute_query "
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
        );
    "
            echo "----------------------------------------"
            ;;
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
