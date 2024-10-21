
### **1. Top 5 Most Borrowed Authors**
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
#### Breakdown:
- **`SELECT`**: Retrieves specific columns from the database. In this case, it retrieves `Author_ID`, `Name`, and a count of how many times their books were borrowed (`COUNT(L.Loan_Number)`).
- **`COUNT()`**: This function counts the number of occurrences of something—in this case, the number of loans (`Loan_Number`) for each author.
- **`FROM Authors A`**: Specifies the table to select data from, using an alias (`A`) for the `Authors` table.
- **`JOIN`**: Joins two tables together:
  - **`BookAuthor BA ON A.Author_ID = BA.Author_ID`**: This joins the `Authors` table to the `BookAuthor` table based on the matching `Author_ID`.
  - **`Loans L ON BA.ISBN = L.ISBN`**: This joins the `BookAuthor` table to the `Loans` table using the `ISBN` field.
- **`GROUP BY`**: Groups the results by `Author_ID` and `Name`, so we get one row per author.
- **`ORDER BY Borrow_Count DESC`**: Orders the results in descending order based on the number of books borrowed (`Borrow_Count`), showing the most borrowed authors first.
- **`FETCH FIRST 5 ROWS ONLY`**: Limits the output to the top 5 rows, showing only the top 5 most borrowed authors.

### **2. Borrowers with Overdue Loans**
```bash
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
```
#### Breakdown:
- **`||`**: Concatenation operator in SQL. Combines `First_Name` and `Last_Name` with a space between them to create a full name (`Borrower_Name`).
- **`TRUNC(SYSDATE - L.Due_Date) AS Days_Overdue`**: `TRUNC()` truncates a value to its integer part. Here, it calculates the number of days a loan is overdue by subtracting the `Due_Date` from the current date (`SYSDATE`).
- **`JOIN`**:
  - `Borrowers BR ON L.Borrower_ID = BR.Borrower_ID`: Joins the `Loans` table with the `Borrowers` table using the `Borrower_ID`.
  - `Users U ON BR.User_ID = U.User_ID`: Joins the `Borrowers` table with the `Users` table to get the user's details.
- **`WHERE L.Return_Status = 'N'`**: Filters the loans to show only the ones where the return status is 'N' (not returned).
- **`AND L.Due_Date < SYSDATE`**: Further filters the loans to show only overdue loans (where the due date is earlier than the current date).
- **`ORDER BY Days_Overdue DESC`**: Sorts the results by the number of overdue days, showing the most overdue loans first.

### **3. Genres with Most Books**
```bash
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
    HAVING COUNT(BG.ISBN) > 1;
"
```
#### Breakdown:
- **`COUNT(BG.ISBN)`**: Counts how many books (`ISBN`s) are associated with each genre.
- **`HAVING`**: Similar to `WHERE`, but used after `GROUP BY` to filter groups based on a condition. In this case, it filters out genres that have only one or zero books.
- **`JOIN BookGenre BG ON G.Genre_ID = BG.Genre_ID`**: Joins the `Genres` table with the `BookGenre` table based on the `Genre_ID`.

### **4. Administrators Managing Most Books**
```bash
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
```
#### Breakdown:
- **`COUNT(B.ISBN)`**: Counts the number of books (`ISBN`s) managed by each administrator.
- **`JOIN`**:
  - `Users U ON A.User_ID = U.User_ID`: Joins the `Administrators` table with the `Users` table to get the admin's full name.
  - `Books B ON A.Admin_ID = B.Admin_ID`: Joins the `Administrators` table with the `Books` table based on the `Admin_ID`.
- **`GROUP BY`**: Groups the results by `Admin_ID` and the admin's name.
- **`ORDER BY Books_Managed DESC`**: Sorts the results by the number of books managed, showing the administrators who manage the most books first.

### **5. Total Fines Collected by Administrators**
```bash
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
```
#### Breakdown:
- **`SUM(L.Fine_Amount)`**: Sums up the total fines collected by each administrator.
- **`JOIN`**:
  - `Users U ON A.User_ID = U.User_ID`: Joins the `Administrators` table with the `Users` table to retrieve admin names.
  - `Loans L ON A.Admin_ID = L.Admin_ID`: Joins the `Administrators` table with the `Loans` table based on the `Admin_ID`.
- **`GROUP BY`**: Groups the results by `Admin_ID` and the admin's name.
- **`ORDER BY Total_Fines_Collected DESC`**: Sorts the results in descending order by the total fines collected.

### **6. Authors with No Borrowed Books**
```bash
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
```
#### Breakdown:
- **`NOT EXISTS`**: This checks whether a subquery returns no results. In this case, it ensures that there are no loans for a given author.
- **`SELECT 1`**: A placeholder in the subquery that doesn’t actually retrieve any data. It simply checks if any rows exist where the author has a book that has been borrowed.
- **`JOIN Loans L ON BA.ISBN = L.ISBN`**: Joins the `BookAuthor` table with the `Loans` table, checking if the author has any books that have been loaned out.

### **7. All Unique Genres (Using UNION)**
```bash
execute_query "
        SELECT Title AS Genre_Title FROM Genres
        UNION
        SELECT DISTINCT G.Title AS Genre_Title FROM Genres G;
"
```
#### Breakdown:
- **`UNION`**: Combines the results of two `SELECT` statements. It removes duplicate rows from the results.
- **`SELECT DISTINCT G.Title`**: Ensures that only unique genre titles are selected from the second query (even though `UNION` already removes duplicates, using `DISTINCT` adds an extra layer of assurance).

### **8. Books Not Borrowed in the Last Year (MINUS)**
```bash
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
```
#### Breakdown:
- **`NOT IN`**: Filters out records where the book’s ISBN appears in the subquery results.
- **`ADD_MONTHS(SYSDATE, -12)`**: Adds (or in this case, subtracts) months from a date. Here it subtracts 12 months from the current date (`SYSDATE`), giving us the date one year ago.
- **Subquery**: The subquery selects all ISBNs of books that have been borrowed in the last year, and the outer query filters out these books, showing only those that haven't been borrowed in the past year.

---

### Summary
Each `execute_query` block embeds an SQL query directly into the script, using Bash's ability to execute multi-line SQL commands through `sqlplus`. The queries use common SQL features like `SELECT`, `JOIN`, `GROUP BY`, `COUNT()`, `SUM()`, `NOT EXISTS`, and `UNION` to retrieve or manipulate information about authors, books, loans, and other aspects of a library management system.