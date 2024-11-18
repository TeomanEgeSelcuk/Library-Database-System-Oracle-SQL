-- create_views.sql

CREATE OR REPLACE VIEW ViewTopBorrowedAuthors AS
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
    A.Author_ID, A.Name;

CREATE OR REPLACE VIEW ViewOverdueLoans AS
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
    AND L.Due_Date < SYSDATE;

CREATE OR REPLACE VIEW ViewGenreBookCount AS
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
