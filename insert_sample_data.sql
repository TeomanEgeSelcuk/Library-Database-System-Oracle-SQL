-- Inserting Sample Data into Tables

-- Inserting sample users into the Users table
INSERT INTO Users (First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code)
VALUES ('John', 'Doe', '123-456-7890', 'john.doe@example.com', 'johndoe', 'password123', '123 Elm St', 'Springfield', 'IL', '62704');

INSERT INTO Users (First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code)
VALUES ('Jane', 'Smith', '987-654-3210', 'jane.smith@example.com', 'janesmith', 'securepass', '456 Oak Ave', 'Lincoln', 'NE', '68508');

-- Inserting sample borrowers into the Borrowers table
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable)
VALUES (1, 1, 5, 0);

INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable)
VALUES (2, 2, 3, 10);

-- Inserting sample administrators into the Administrators table
INSERT INTO Administrators (Admin_ID, User_ID, Role, Permissions, Last_Login)
VALUES (1, 1, 'Library Manager', 'ALL', TO_DATE('2024-04-01', 'YYYY-MM-DD'));

INSERT INTO Administrators (Admin_ID, User_ID, Role, Permissions, Last_Login)
VALUES (2, 2, 'Assistant Manager', 'READ, WRITE', TO_DATE('2024-04-15', 'YYYY-MM-DD'));

-- Inserting sample authors into the Authors table
INSERT INTO Authors (Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES ('George Orwell', 'English novelist and essayist.', TO_DATE('1903-06-25', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Name, Biography, Date_of_Birth, Nationality, Languages)
VALUES ('J.K. Rowling', 'British author, best known for the Harry Potter series.', TO_DATE('1965-07-31', 'YYYY-MM-DD'), 'British', 'English');

-- Inserting sample genres into the Genres table
INSERT INTO Genres (Title, Description)
VALUES ('Fiction', 'Literary works based on the imagination and not strictly on history or fact.');

INSERT INTO Genres (Title, Description)
VALUES ('Science Fiction', 'Fiction dealing with futuristic concepts such as advanced science and technology.');

-- Inserting sample books into the Books table
INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0451524935', '1984', TO_DATE('1949-06-08', 'YYYY-MM-DD'), 328, 5, 'Secker & Warburg', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID)
VALUES ('978-0545582889', 'Harry Potter and the Sorcerer''s Stone', TO_DATE('1997-06-26', 'YYYY-MM-DD'), 309, 10, 'Bloomsbury', 2);

-- Inserting relationships between books and authors into the BookAuthor table
INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0451524935', 1);

INSERT INTO BookAuthor (ISBN, Author_ID)
VALUES ('978-0545582889', 2);

-- Inserting relationships between books and genres into the BookGenre table
INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0451524935', 1);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0451524935', 2);

INSERT INTO BookGenre (ISBN, Genre_ID)
VALUES ('978-0545582889', 1);

-- Inserting sample loans into the Loans table
INSERT INTO Loans (Borrower_ID, ISBN, Due_Date, Return_Status, Admin_ID)
VALUES (1, '978-0451524935', TO_DATE('2024-05-15', 'YYYY-MM-DD'), 'N', 1);

INSERT INTO Loans (Borrower_ID, ISBN, Due_Date, Return_Status, Admin_ID)
VALUES (2, '978-0545582889', TO_DATE('2024-05-20', 'YYYY-MM-DD'), 'Y', 2);


-- Inserting additional borrowers with overdue loans

-- Inserting a new user
INSERT INTO Users (
    First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code
)
VALUES (
    'Alice', 'Johnson', '555-123-4567', 'alice.johnson@example.com', 'alicej', 'alicepass', 
    '789 Pine Rd', 'Madison', 'WI', '53703'
);  -- Added missing semicolon

-- Inserting a new borrower
INSERT INTO Borrowers (
    Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable
)
VALUES (
    3, 3, 4, 15
);

-- Inserting a new loan that is overdue
INSERT INTO Loans (
    Borrower_ID, ISBN, Due_Date, Return_Status, Admin_ID
)
VALUES (
    3, '978-0545582889', TO_DATE('2024-09-01', 'YYYY-MM-DD'), 'N', 2
);




