# Library Database System

## Table of Contents

- [Abstract](#abstract)
- [Introduction](#introduction)
- [Features](#features)
- [ER Model](#er-model)
- [Schema Design](#schema-design)
- [Database Construction and SQL Queries](#database-construction-and-sql-queries)
- [Advanced Queries and Scripts](#advanced-queries-and-scripts)
  - [Unix Shell Scripts](#unix-shell-scripts)
  - [Python Scripts](#python-scripts)
- [Normalization](#normalization)
- [Final Documentation](#final-documentation)
- [Project Demo](#project-demo)
- [Conclusion](#conclusion)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Shell Menu](#running-the-shell-menu)
  - [Running the Python Interface](#running-the-python-interface)
- [Contributing](#contributing)
- [License](#license)

## Abstract

This project focuses on the design and implementation of a comprehensive relational database system for managing the operations of a library. The system handles key entities such as users, borrowers, administrators, books, authors, genres, and loans. It ensures efficient management of borrowing activities, including tracking loan records, overdue fines, and book availability. The database categorizes books by genre and author, adhering to normalization principles to ensure data integrity and minimize redundancy. Key features include detailed constraints, such as primary and foreign key relationships, and check constraints to maintain data accuracy. The final design supports scalable and efficient querying, laying the foundation for a fully functional library management system capable of future expansions, such as a user-friendly interface for library staff and members.

## Introduction

### Project Overview

The Library Database System is designed to streamline and manage the various operations within a library. It provides a structured approach to handling book inventories, user information, borrowing processes, and administrative tasks.

### Goals and Objectives

- **Adherence to SQL Standards:** Implement a database that follows SQL standards, including normalization up to the Third Normal Form (3NF).
- **Essential Library Operations:** Support functionalities such as book lending, fine management, and user tracking.
- **Data Integrity:** Ensure data accuracy and consistency through the use of primary and foreign keys, as well as check constraints.

### Scope

The system encompasses features for:

- Managing user information, borrowing limits, and payment history.
- Organizing book details, including authors, genres, and availability.
- Tracking loans, return statuses, due dates, and fines.
- Administering book management and enforcing borrowing rules.

## Features

- **User Management:** Handles registration, authentication, and profile management for borrowers and administrators.
- **Book Tracking:** Manages book details, availability, and categorization by authors and genres.
- **Loan Processing:** Facilitates borrowing and returning of books, tracking due dates, and calculating overdue fines.
- **Administrative Controls:** Allows administrators to manage books, authors, genres, borrowers, and oversee loan activities.
- **Advanced Querying:** Supports complex SQL queries for reporting and data analysis.
- **Scripts for Automation:** Implements both Unix shell scripts and Python scripts for database interactions and menu-driven operations.
- **Python CLI Interface:** Provides a more advanced and user-friendly command-line interface using Python for interacting with the database.

## ER Model

The Entity-Relationship (ER) diagram below illustrates the structure of the Library Database System, showcasing the entities and their relationships.

![image](https://github.com/user-attachments/assets/9439863d-a9ff-4eb2-8565-1fd4c461c65e)

## Schema Design

The database schema is derived from the ER diagram and defines the structure of the tables, their attributes, and relationships.

### Entities and Tables

- **User**
  - **Attributes:** UserID (PK), FirstName, LastName, PhoneNumber, Email, Username, Password, Street, City, State, ZIP
- **Borrower**
  - **Attributes:** BorrowerID (PK, FK to UserID), BorrowingLimit, AmountPayable
- **Administrator**
  - **Attributes:** AdminID (PK, FK to UserID), Role, Permissions, LastLogin
- **Book**
  - **Attributes:** ISBN (PK), Title, PublicationDate, Pages, CopiesAvailable, Publisher
- **Author**
  - **Attributes:** AuthorID (PK), Name, Biography, DateOfBirth, DateOfDeath, Nationality
- **Genre**
  - **Attributes:** GenreID (PK), Title, Description
- **Loan**
  - **Attributes:** LoanNumber (PK), BorrowerID (FK), ISBN (FK), LoanDate, DueDate, ReturnDate, FineAmount, ReturnStatus
- **BookAuthor**
  - **Attributes:** ISBN (PK, FK), AuthorID (PK, FK)
- **BookGenre**
  - **Attributes:** ISBN (PK, FK), GenreID (PK, FK)

### Relationships

- **Books ↔ Authors:** Many-to-many
- **Books ↔ Genres:** Many-to-many
- **Borrowers ↔ Loans:** One-to-many
- **Loans ↔ Books:** One-to-many
- **Administrators ↔ All Entities:** One-to-many

## Database Construction and SQL Queries

The database was constructed using Oracle SQL, implementing all tables, relationships, and constraints as per the schema design. A series of SQL queries were developed to perform both basic and advanced operations, including joins, aggregations, and views. These queries facilitate efficient data retrieval and management within the library system.

## Advanced Queries and Scripts

### Unix Shell Scripts

Advanced SQL queries were complemented by Unix shell scripts to create a menu-driven interface, allowing users to interact with the database seamlessly. These scripts handle operations such as searching for books, managing loans, and generating reports through simple command-line menus.

#### Example Shell Menu

```bash
#!/bin/bash

echo "Library Database System"
echo "1. Find Top 5 Most Borrowed Authors"
echo "2. List Overdue Loans"
echo "3. Find Genres with Most Books"
echo "4. List Administrators Managing Most Books"
echo "5. Show Total Fines Collected by Administrators"
echo "6. Find Authors with No Borrowed Books"
echo "7. List Unique Genres"
echo "8. Show Books Not Borrowed in the Last Year"
echo "9. Search Records"
echo "10. Add Records"
echo "11. Update Records"
echo "12. Delete Records"
echo "13. Relational Algebra"
echo "0. Exit"

read -p "Select an option: " option

case $option in
    1) # Execute SQL query for top 5 authors ;;
    2) # Execute SQL query for overdue loans ;;
    # Add cases for other options
    0) exit ;;
    *) echo "Invalid option" ;;
esac
```

### Python Scripts

To enhance user experience and provide a more robust command-line interface, Python scripts have been developed. These scripts offer better error handling, input validation, and a more intuitive navigation system compared to the Unix shell scripts.

#### Example Python CLI Interface

```python
import sys
import cx_Oracle

def connect_db():
    try:
        connection = cx_Oracle.connect("username", "password", "hostname/SID")
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)

def find_top_authors(connection):
    cursor = connection.cursor()
    query = """
    SELECT Author_ID, Name, COUNT(Loan_Number) AS Borrow_Count
    FROM Authors
    JOIN BookAuthor ON Authors.Author_ID = BookAuthor.Author_ID
    JOIN Loans ON BookAuthor.ISBN = Loans.ISBN
    GROUP BY Author_ID, Name
    ORDER BY Borrow_Count DESC
    FETCH FIRST 5 ROWS ONLY
    """
    cursor.execute(query)
    for row in cursor:
        print(row)
    cursor.close()

def main_menu():
    connection = connect_db()
    while True:
        print("\nLibrary Database System - Python CLI")
        print("1. Find Top 5 Most Borrowed Authors")
        print("2. List Overdue Loans")
        print("3. Find Genres with Most Books")
        print("4. List Administrators Managing Most Books")
        print("5. Show Total Fines Collected by Administrators")
        print("6. Find Authors with No Borrowed Books")
        print("7. List Unique Genres")
        print("8. Show Books Not Borrowed in the Last Year")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            find_top_authors(connection)
        elif choice == '2':
            # Implement the function for listing overdue loans
            pass
        elif choice == '3':
            # Implement the function for finding genres with most books
            pass
        elif choice == '4':
            # Implement the function for listing administrators managing most books
            pass
        elif choice == '5':
            # Implement the function for showing total fines collected by administrators
            pass
        elif choice == '6':
            # Implement the function for finding authors with no borrowed books
            pass
        elif choice == '7':
            # Implement the function for listing unique genres
            pass
        elif choice == '8':
            # Implement the function for showing books not borrowed in the last year
            pass
        elif choice == '0':
            print("Exiting...")
            connection.close()
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
```

## Normalization

The database design adheres to normalization principles to ensure data integrity and eliminate redundancy.

### Functional Dependencies

Detailed functional dependencies were established for each table to guide the normalization process.

### Normalization to Third Normal Form (3NF)

- **1NF:** Ensured atomicity of all table columns.
- **2NF:** Eliminated partial dependencies by ensuring all non-key attributes are fully functionally dependent on the primary key.
- **3NF:** Removed transitive dependencies, ensuring that non-key attributes depend only on the primary key.

### Normalization to BCNF

The database was further normalized to Boyce-Codd Normal Form (BCNF) to eliminate any remaining anomalies:

- **Books Table:** Decomposed to separate publisher details.
- **Loans Table:** Decomposed to separate fine management.

All tables now conform to BCNF, ensuring optimal database structure.

## Final Documentation

### Relational Algebra Queries

1. **Find Top 5 Most Borrowed Authors**
   ```sql
   SELECT Author_ID, Name, COUNT(Loan_Number) AS Borrow_Count
   FROM Authors
   JOIN BookAuthor ON Authors.Author_ID = BookAuthor.Author_ID
   JOIN Loans ON BookAuthor.ISBN = Loans.ISBN
   GROUP BY Author_ID, Name
   ORDER BY Borrow_Count DESC
   FETCH FIRST 5 ROWS ONLY;
   ```
2. **List Overdue Loans**
   ```sql
   SELECT Loans.*, Borrowers.*, Users.*
   FROM Loans
   JOIN Borrowers ON Loans.Borrower_ID = Borrowers.Borrower_ID
   JOIN Users ON Borrowers.User_ID = Users.User_ID
   WHERE Return_Status = 'N' AND Due_Date < SYSDATE
   ORDER BY (SYSDATE - Due_Date) DESC;
   ```
3. **Find Genres with Most Books**
   ```sql
   SELECT Genre_ID, Title, COUNT(ISBN) AS Number_of_Books
   FROM Genres
   JOIN BookGenre ON Genres.Genre_ID = BookGenre.Genre_ID
   GROUP BY Genre_ID, Title
   HAVING COUNT(ISBN) > 1
   ORDER BY Number_of_Books DESC;
   ```
4. **List Administrators Managing Most Books**
   ```sql
   SELECT Admin_ID, Admin_Name, COUNT(ISBN) AS Books_Managed
   FROM Administrators
   JOIN Users ON Administrators.User_ID = Users.User_ID
   JOIN Books ON Administrators.Admin_ID = Books.Admin_ID
   GROUP BY Admin_ID, Admin_Name
   ORDER BY Books_Managed DESC;
   ```
5. **Show Total Fines Collected by Administrators**
   ```sql
   SELECT Admin_ID, Admin_Name, SUM(Fine_Amount) AS Total_Fines
   FROM Administrators
   JOIN Users ON Administrators.User_ID = Users.User_ID
   JOIN Loans ON Administrators.Admin_ID = Loans.Admin_ID
   GROUP BY Admin_ID, Admin_Name
   ORDER BY Total_Fines DESC;
   ```
6. **Find Authors with No Borrowed Books**
   ```sql
   SELECT Author_ID, Name
   FROM Authors
   WHERE Author_ID NOT IN (
       SELECT BookAuthor.Author_ID
       FROM BookAuthor
       JOIN Loans ON BookAuthor.ISBN = Loans.ISBN
   );
   ```
7. **List Unique Genres**
   ```sql
   SELECT DISTINCT Title
   FROM Genres;
   ```
8. **Show Books Not Borrowed in the Last Year**
   ```sql
   SELECT ISBN, Title
   FROM Books
   WHERE ISBN NOT IN (
       SELECT ISBN
       FROM Loans
       WHERE Loan_Date >= ADD_MONTHS(SYSDATE, -12)
   );
   ```

## Project Demo

A demonstration of the Library Database System showcases the functionality of the system through various menu options, illustrating how users can interact with the database to perform operations such as searching for books, managing loans, and generating reports.

![image](https://github.com/user-attachments/assets/50f8a514-e0e9-4bf3-966a-64e4bc835e87)

*Figure: Login Menu for Access to Library Management System*

![image](https://github.com/user-attachments/assets/1ca4807e-64fe-4d89-8f12-2c53011b0c27)

*Figure: Main Menu of Library Database System*

![image](https://github.com/user-attachments/assets/72df236f-2bf1-4e5a-bab7-8c7d8fbc7ece)

*Figure: Menu Option 7; Finding Top 5 Most Borrowed Authors*

![image](https://github.com/user-attachments/assets/3ea1ed44-ee0d-4f7d-9ec5-a689b6ccfa14)

*Figure: Menu Option 8; Listing Overdue Loans with Days Overdue*

<!-- Add more images as needed -->

## Conclusion

The Library Database System project successfully developed a robust and scalable database solution for managing library operations. Through collaborative efforts, the team overcame challenges related to group coordination and technical hurdles with shell scripting and Python integration. The resulting system demonstrates effective database design, normalization, and query implementation, providing a solid foundation for future enhancements such as a graphical user interface.

## Installation

### Prerequisites

- **Oracle Database:** Ensure Oracle Database is installed and running on your system.
- **SQL Developer:** Optional, for database management and query execution.
- **Unix Shell:** For running shell scripts (Linux or macOS recommended).
- **Python 3.x:** Required for running the Python CLI interface.
- **cx_Oracle:** Python library for Oracle Database connectivity.

### Setup Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/TeomanEgeSelcuk/Library-Database-System-Oracle-SQL.git
   cd Library-Database-System-Oracle-SQL
   ```

2. **Create the Database Schema:**
   - Open Oracle SQL Developer or your preferred SQL client.
   - Execute the `schema.sql` script to create tables and relationships.
     ```sql
     @schema.sql
     ```

3. **Populate the Database:**
   - Execute the `data.sql` script to insert initial data.
     ```sql
     @data.sql
     ```

4. **Configure Shell Scripts:**
   - Ensure shell scripts have execute permissions.
     ```bash
     chmod +x sql_commands.sh
     ```

5. **Set Up Python Environment:**
   - Install required Python packages.
     ```bash
     pip install cx_Oracle
     ```
   - Configure Oracle Client libraries if necessary. Refer to [cx_Oracle Installation](https://cx-oracle.readthedocs.io/en/latest/installation.html) for detailed instructions.

## Usage

### Running the Shell Menu

1. **Navigate to the Project Directory:**
   ```bash
   cd Library-Database-System-Oracle-SQL
   ```

2. **Run the Shell Script:**
   ```bash
   ./sql_commands.sh
   ```

3. **Select an Option:**
   - Follow the on-screen prompts to perform various operations such as searching for books, managing loans, and generating reports.

### Running the Python Interface

1. **Navigate to the Project Directory:**
   ```bash
   cd Library-Database-System-Oracle-SQL
   ```

2. **Run the Python Script:**
   ```bash
   python3 sql_commands.py
   ```

3. **Select an Option:**
   - Use the Python CLI to interact with the database through a more advanced and user-friendly interface.
   - Options include finding top borrowed authors, listing overdue loans, managing genres, and more.


# Conclusion

This comprehensive README provides all necessary information to understand, install, and use the Library Database System. By incorporating both Unix shell scripts and Python scripts, the system caters to different user preferences, ensuring flexibility and ease of use. The detailed documentation, including ER diagrams and example queries, facilitates easy navigation and understanding of the project's structure and functionalities.
