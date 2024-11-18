-- Deleting All Data from Tables

-- Delete all records from the Loans table
DELETE FROM Loans;
-- Alternatively, you can use TRUNCATE for faster deletion without logging individual row deletions
-- TRUNCATE TABLE Loans;

-- Delete all records from the BookGenre table
DELETE FROM BookGenre;
-- TRUNCATE TABLE BookGenre;

-- Delete all records from the BookAuthor table
DELETE FROM BookAuthor;
-- TRUNCATE TABLE BookAuthor;

-- Delete all records from the Books table
DELETE FROM Books;
-- TRUNCATE TABLE Books;

-- Delete all records from the Genres table
DELETE FROM Genres;
-- TRUNCATE TABLE Genres;

-- Delete all records from the Authors table
DELETE FROM Authors;
-- TRUNCATE TABLE Authors;

-- Delete all records from the Administrators table
DELETE FROM Administrators;
-- TRUNCATE TABLE Administrators;

-- Delete all records from the Borrowers table
DELETE FROM Borrowers;
-- TRUNCATE TABLE Borrowers;

-- Delete all records from the Users table
DELETE FROM Users;
-- TRUNCATE TABLE Users;

-- Commit the deletions to make sure all changes are saved
COMMIT;
