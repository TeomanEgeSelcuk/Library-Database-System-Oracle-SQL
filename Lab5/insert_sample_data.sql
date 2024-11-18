-- Disable substitution variable prompting
SET DEFINE OFF;

-- Inserting Sample Data into Tables

-- Inserting sample users into the Users table
INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code)
VALUES (1, 'John', 'Doe', '123-456-7890', 'john.doe@example.com', 'johndoe', 'password123', '123 Elm St', 'Springfield', 'IL', '62704');

INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code)
VALUES (2, 'Jane', 'Smith', '987-654-3210', 'jane.smith@example.com', 'janesmith', 'securepass', '456 Oak Ave', 'Lincoln', 'NE', '68508');

-- Inserting additional users to prevent duplicate IDs
INSERT INTO Users (
    User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code
)
VALUES (
    3, 'Alice', 'Johnson', '555-123-4567', 'alice.johnson@example.com', 'alicej', 'alicepass', 
    '789 Pine Rd', 'Madison', 'WI', '53703'
);

-- Inserting sample borrowers into the Borrowers table
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable)
VALUES (1, 1, 5, 0);

INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable)
VALUES (2, 2, 3, 10);

INSERT INTO Borrowers (
    Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable
)
VALUES (
    3, 3, 4, 15
);

-- Inserting sample administrators into the Administrators table
INSERT INTO Administrators (Admin_ID, User_ID, Role, Permissions, Last_Login)
VALUES (1, 1, 'Library Manager', 'ALL', TO_DATE('2024-04-01', 'YYYY-MM-DD'));

INSERT INTO Administrators (Admin_ID, User_ID, Role, Permissions, Last_Login)
VALUES (2, 2, 'Assistant Manager', 'READ, WRITE', TO_DATE('2024-04-15', 'YYYY-MM-DD'));

-- Inserting sample authors into the Authors table
INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES (1, 'George Orwell', 'English novelist and essayist.', TO_DATE('1903-06-25', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES (2, 'J.K. Rowling', 'British author, best known for the Harry Potter series.', TO_DATE('1965-07-31', 'YYYY-MM-DD'), 'British', 'English');

-- Adding a new author whose books have not been borrowed (for Query 12)
INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES (3, 'Aldous Huxley', 'English writer and philosopher.', TO_DATE('1894-07-26', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES (4, 'Frank Herbert', 'American science fiction author.', TO_DATE('1920-10-08', 'YYYY-MM-DD'), 'American', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES (5, 'Harper Lee', 'American novelist widely known for To Kill a Mockingbird.', TO_DATE('1926-04-28', 'YYYY-MM-DD'), 'American', 'English');

-- Inserting sample genres into the Genres table
INSERT INTO Genres (Genre_ID, Title, Description)
VALUES (1, 'Fiction', 'Literary works based on the imagination and not strictly on history or fact.');

INSERT INTO Genres (Genre_ID, Title, Description)
VALUES (2, 'Science Fiction', 'Fiction dealing with futuristic concepts such as advanced science and technology.');

-- Adding an additional genre 'Mystery'
INSERT INTO Genres (Genre_ID, Title, Description)
VALUES (3, 'Mystery', 'Fiction genre involving solving a crime or unraveling secrets.');

-- Inserting sample books into the Books table
INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0451524935', '1984', TO_DATE('1949-06-08', 'YYYY-MM-DD'), 328, 5, q'[Secker & Warburg]', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0545582889', 'Harry Potter and the Sorcerer''s Stone', TO_DATE('1997-06-26', 'YYYY-MM-DD'), 309, 10, 'Bloomsbury', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0060850524', 'Brave New World', TO_DATE('1932-01-01', 'YYYY-MM-DD'), 268, 4, q'[Chatto & Windus]', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0441013593', 'Dune', TO_DATE('1965-08-01', 'YYYY-MM-DD'), 412, 7, 'Chilton Books', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0061120084', 'To Kill a Mockingbird', TO_DATE('1960-07-11', 'YYYY-MM-DD'), 281, 6, q'[J.B. Lippincott & Co.]', 2);

-- Inserting an additional book for the 'Mystery' genre
INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-1234567890', 'The Hound of the Baskervilles', TO_DATE('1902-04-01', 'YYYY-MM-DD'), 256, 3, q'[George Newnes Ltd.]', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0987654321', 'Gone Girl', TO_DATE('2012-06-05', 'YYYY-MM-DD'), 422, 4, 'Crown Publishing Group', 2);

-- Inserting relationships between books and authors into the BookAuthor table
INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0451524935', 1);

INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0545582889', 2);

INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0060850524', 3);

INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0441013593', 4);

INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0061120084', 5);

-- Associating the new books with authors (assuming correct author IDs)
INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-1234567890', 1);  -- George Orwell (for demonstration purposes)

INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0987654321', 5);  -- Harper Lee (for demonstration purposes)

-- Inserting relationships between books and genres into the BookGenre table
INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0451524935', 1);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0451524935', 2);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0545582889', 1);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0060850524', 2);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0441013593', 2);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0061120084', 1);  -- 'Fiction' genre

-- Associating the new books with 'Mystery' genre
INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-1234567890', 3);  -- 'The Hound of the Baskervilles' in 'Mystery'

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0987654321', 3);  -- 'Gone Girl' in 'Mystery'

-- Inserting sample loans into the Loans table
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID)
VALUES (1, 1, '978-0451524935', TO_DATE('2024-05-15', 'YYYY-MM-DD'), TO_DATE('2024-05-30', 'YYYY-MM-DD'), 'N', 1);

INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID)
VALUES (2, 2, '978-0545582889', TO_DATE('2024-05-20', 'YYYY-MM-DD'), TO_DATE('2024-06-04', 'YYYY-MM-DD'), 'Y', 2);

-- Creating a loan for 'Dune' that was over a year ago (so it appears in Query 14)
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID)
VALUES (
    3, 
    1, 
    '978-0441013593', 
    ADD_MONTHS(SYSDATE, -15),  -- Loaned 15 months ago
    ADD_MONTHS(SYSDATE, -13),  -- Due 13 months ago
    'Y', 
    1
);

-- Re-enable substitution variables if needed elsewhere
SET DEFINE ON;
