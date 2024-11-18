-- ========================
-- Inserting Sample Data into Tables
-- ========================

-- 1. Inserting sample users into the Users table
INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code) VALUES
(1, 'John', 'Doe', '123-456-7890', 'john.doe@example.com', 'johndoe', 'password123', '123 Elm St', 'Springfield', 'IL', '62704');

INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code) VALUES
(2, 'Jane', 'Smith', '987-654-3210', 'jane.smith@example.com', 'janesmith', 'securepass', '456 Oak Ave', 'Lincoln', 'NE', '68508');

INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code) VALUES
(3, 'Alice', 'Johnson', '555-123-4567', 'alice.johnson@example.com', 'alicej', 'alicepass', '789 Pine Rd', 'Madison', 'WI', '53703');

INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code) VALUES
(4, 'Bob', 'Brown', '111-222-3333', 'bob.brown@example.com', 'bobbrown', 'password456', '101 Maple St', 'Columbus', 'OH', '43215');

INSERT INTO Users (User_ID, First_Name, Last_Name, Phone_Number, Email, Username, Password, Street, City, State, ZIP_Code) VALUES
(5, 'Sara', 'Connor', '222-333-4444', 'sara.connor@example.com', 'saraconnor', 'terminator', '2020 Future Rd', 'Los Angeles', 'CA', '90001');

-- 2. Inserting sample administrators into the Administrators table
INSERT INTO Administrators (Admin_ID, User_ID, Role, Permissions, Last_Login) VALUES
(1, 1, 'Library Manager', 'ALL', TO_DATE('2024-04-01', 'YYYY-MM-DD'));

INSERT INTO Administrators (Admin_ID, User_ID, Role, Permissions, Last_Login) VALUES
(2, 2, 'Assistant Manager', 'READ, WRITE', TO_DATE('2024-04-15', 'YYYY-MM-DD'));

-- 3. Inserting sample borrowers into the Borrowers table
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable) VALUES (3, 3, 4, 15);
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable) VALUES (4, 4, 5, 0);
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable) VALUES (5, 5, 5, 0);

-- Note: Users 1 and 2 are administrators and also borrowers
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable) VALUES (1, 1, 5, 0);
INSERT INTO Borrowers (Borrower_ID, User_ID, Borrowing_Limit, Amount_Payable) VALUES (2, 2, 3, 10);

-- 4. Inserting sample authors into the Authors table
INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(1, 'George Orwell', 'English novelist and essayist.', TO_DATE('1903-06-25', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(2, 'J.K. Rowling', 'British author, best known for the Harry Potter series.', TO_DATE('1965-07-31', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(3, 'Aldous Huxley', 'English writer and philosopher.', TO_DATE('1894-07-26', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(4, 'Frank Herbert', 'American science fiction author.', TO_DATE('1920-10-08', 'YYYY-MM-DD'), 'American', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(5, 'Harper Lee', 'American novelist widely known for To Kill a Mockingbird.', TO_DATE('1926-04-28', 'YYYY-MM-DD'), 'American', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(6, 'Arthur Conan Doyle', 'British writer best known for Sherlock Holmes stories.', TO_DATE('1859-05-22', 'YYYY-MM-DD'), 'British', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(7, 'Gillian Flynn', 'American author and screenwriter.', TO_DATE('1971-02-24', 'YYYY-MM-DD'), 'American', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(8, 'Isaac Asimov', 'American writer and professor of biochemistry.', TO_DATE('1920-01-02', 'YYYY-MM-DD'), 'American', 'English');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(9, 'Stieg Larsson', 'Swedish journalist and writer.', TO_DATE('1954-08-15', 'YYYY-MM-DD'), 'Swedish', 'Swedish');

INSERT INTO Authors (Author_ID, Name, Biography, Date_of_Birth, Nationality, Languages) VALUES
(10, 'J.R.R. Tolkien', 'English writer, poet, philologist, and academic.', TO_DATE('1892-01-03', 'YYYY-MM-DD'), 'British', 'English');

-- 5. Inserting sample genres into the Genres table
INSERT INTO Genres (Genre_ID, Title, Description) VALUES
(1, 'Fiction', 'Literary works based on the imagination and not strictly on history or fact.');

INSERT INTO Genres (Genre_ID, Title, Description) VALUES
(2, 'Science Fiction', 'Fiction dealing with futuristic concepts such as advanced science and technology.');

INSERT INTO Genres (Genre_ID, Title, Description) VALUES
(3, 'Mystery', 'Fiction genre involving solving a crime or unraveling secrets.');

INSERT INTO Genres (Genre_ID, Title, Description) VALUES
(4, 'Fantasy', 'Fiction with magical or supernatural elements.');

-- 6. Inserting sample books into the Books table
-- Note: Replace '&' with 'and' in publisher names to avoid substitution variable issues

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0451524935', '1984', TO_DATE('1949-06-08', 'YYYY-MM-DD'), 328, 5, 'Secker and Warburg', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0545582889', 'Harry Potter and the Sorcerer''s Stone', TO_DATE('1997-06-26', 'YYYY-MM-DD'), 309, 10, 'Bloomsbury', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0060850524', 'Brave New World', TO_DATE('1932-01-01', 'YYYY-MM-DD'), 268, 4, 'Chatto and Windus', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0441013593', 'Dune', TO_DATE('1965-08-01', 'YYYY-MM-DD'), 412, 7, 'Chilton Books', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0061120084', 'To Kill a Mockingbird', TO_DATE('1960-07-11', 'YYYY-MM-DD'), 281, 6, 'J.B. Lippincott and Co.', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-1234567890', 'The Hound of the Baskervilles', TO_DATE('1902-04-01', 'YYYY-MM-DD'), 256, 3, 'George Newnes Ltd.', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0987654321', 'Gone Girl', TO_DATE('2012-06-05', 'YYYY-MM-DD'), 422, 4, 'Crown Publishing Group', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0747532743', 'Harry Potter and the Chamber of Secrets', TO_DATE('1998-07-02', 'YYYY-MM-DD'), 341, 8, 'Bloomsbury', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0553283686', 'Foundation', TO_DATE('1951-05-01', 'YYYY-MM-DD'), 255, 5, 'Gnome Press', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0439136365', 'Harry Potter and the Prisoner of Azkaban', TO_DATE('1999-07-08', 'YYYY-MM-DD'), 435, 8, 'Bloomsbury', 2);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0307454546', 'The Girl with the Dragon Tattoo', TO_DATE('2005-08-01', 'YYYY-MM-DD'), 465, 5, 'Norstedts Forlag', 1);

INSERT INTO Books (ISBN, Title, Publication_Date, Pages, Copies_Available, Publisher, Admin_ID) VALUES
('978-0547928227', 'The Hobbit', TO_DATE('1937-09-21', 'YYYY-MM-DD'), 310, 6, 'George Allen and Unwin', 2);

-- 7. Inserting relationships between books and authors into the BookAuthor table
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0451524935', 1);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0545582889', 2);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0060850524', 3);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0441013593', 4);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0061120084', 5);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-1234567890', 6);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0987654321', 7);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0747532743', 2);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0553283686', 8);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0439136365', 2);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0307454546', 9);
INSERT INTO BookAuthor (ISBN, Author_ID) VALUES ('978-0547928227', 10);

-- 8. Inserting relationships between books and genres into the BookGenre table
INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0451524935', 1);
INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0451524935', 2);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0545582889', 1);
INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0545582889', 4);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0060850524', 2);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0441013593', 2);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0061120084', 1);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-1234567890', 3);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0987654321', 3);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0747532743', 1);
INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0747532743', 4);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0553283686', 2);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0439136365', 1);
INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0439136365', 4);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0307454546', 3);

INSERT INTO BookGenre (ISBN, Genre_ID) VALUES ('978-0547928227', 4);

-- 9. Inserting sample loans into the Loans table
-- Ensure that Borrower_ID, ISBN, and Admin_ID exist before inserting loans

-- Loan 1
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(1, 1, '978-0451524935', TO_DATE('2024-05-15', 'YYYY-MM-DD'), TO_DATE('2024-05-30', 'YYYY-MM-DD'), 'N', 1);

-- Loan 2
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(2, 2, '978-0545582889', TO_DATE('2024-05-20', 'YYYY-MM-DD'), TO_DATE('2024-06-04', 'YYYY-MM-DD'), 'Y', 2);

-- Loan 3
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(3, 1, '978-0441013593', ADD_MONTHS(SYSDATE, -15), ADD_MONTHS(SYSDATE, -13), 'Y', 1);

-- Loan 4 (Bob returned late)
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Date, Fine_Amount, Return_Status, Admin_ID) VALUES
(4, 4, '978-0451524935', TO_DATE('2024-05-01', 'YYYY-MM-DD'), TO_DATE('2024-05-15', 'YYYY-MM-DD'), TO_DATE('2024-05-20', 'YYYY-MM-DD'), 5, 'Y', 1);

-- Update Amount_Payable for Borrower 4
UPDATE Borrowers SET Amount_Payable = Amount_Payable + 5 WHERE Borrower_ID = 4;

-- Simulate payment of the fine for Borrower 4
UPDATE Borrowers SET Amount_Payable = 0 WHERE Borrower_ID = 4;

-- Loan 5 (Sara returned late)
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Date, Fine_Amount, Return_Status, Admin_ID) VALUES
(5, 5, '978-0060850524', TO_DATE('2024-04-10', 'YYYY-MM-DD'), TO_DATE('2024-04-25', 'YYYY-MM-DD'), TO_DATE('2024-05-05', 'YYYY-MM-DD'), 10, 'Y', 2);

-- Update Amount_Payable for Borrower 5
UPDATE Borrowers SET Amount_Payable = Amount_Payable + 10 WHERE Borrower_ID = 5;

-- Simulate payment of the fine for Borrower 5
UPDATE Borrowers SET Amount_Payable = 0 WHERE Borrower_ID = 5;

-- Loan 6
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(6, 2, '978-0747532743', TO_DATE('2024-05-25', 'YYYY-MM-DD'), TO_DATE('2024-06-10', 'YYYY-MM-DD'), 'Y', 2);

-- Loan 7
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(7, 3, '978-0553283686', TO_DATE('2024-05-20', 'YYYY-MM-DD'), TO_DATE('2024-06-05', 'YYYY-MM-DD'), 'Y', 1);

-- Loan 8
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(8, 4, '978-0987654321', TO_DATE('2024-06-01', 'YYYY-MM-DD'), TO_DATE('2024-06-15', 'YYYY-MM-DD'), 'N', 2);

-- Loan 9
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(9, 5, '978-1234567890', TO_DATE('2024-06-05', 'YYYY-MM-DD'), TO_DATE('2024-06-20', 'YYYY-MM-DD'), 'N', 1);

-- Loan 10
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(10, 2, '978-0439136365', TO_DATE('2024-06-10', 'YYYY-MM-DD'), TO_DATE('2024-06-25', 'YYYY-MM-DD'), 'Y', 2);

-- Loan 11
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(11, 3, '978-0439136365', TO_DATE('2024-06-15', 'YYYY-MM-DD'), TO_DATE('2024-06-30', 'YYYY-MM-DD'), 'N', 1);

-- Loan 12
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(12, 3, '978-0307454546', TO_DATE('2024-06-20', 'YYYY-MM-DD'), TO_DATE('2024-07-05', 'YYYY-MM-DD'), 'N', 1);

-- Loan 13
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(13, 4, '978-0547928227', TO_DATE('2024-06-22', 'YYYY-MM-DD'), TO_DATE('2024-07-07', 'YYYY-MM-DD'), 'N', 2);

-- Loan 14
INSERT INTO Loans (Loan_Number, Borrower_ID, ISBN, Loan_Date, Due_Date, Return_Status, Admin_ID) VALUES
(14, 5, '978-0451524935', TO_DATE('2024-06-25', 'YYYY-MM-DD'), TO_DATE('2024-07-10', 'YYYY-MM-DD'), 'N', 1);

-- Commit all the transactions to make data visible
COMMIT;

-- Re-enable substitution variables if needed elsewhere
SET DEFINE ON;