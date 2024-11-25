
-- ========================
-- CREATE TABLE Statements
-- ========================

-- Users table
CREATE TABLE Users (
    User_ID NUMBER PRIMARY KEY,
    First_Name VARCHAR2(50) NOT NULL,
    Last_Name VARCHAR2(50) NOT NULL,
    Phone_Number VARCHAR2(20),
    Email VARCHAR2(100) UNIQUE,
    Username VARCHAR2(50) UNIQUE NOT NULL,
    Password VARCHAR2(255) NOT NULL,
    Street VARCHAR2(100),
    City VARCHAR2(50),
    State VARCHAR2(50),
    ZIP_Code VARCHAR2(10)
);

-- Borrowers table
CREATE TABLE Borrowers (
    Borrower_ID NUMBER PRIMARY KEY,
    User_ID NUMBER UNIQUE,
    Borrowing_Limit NUMBER DEFAULT 5 CHECK (Borrowing_Limit > 0),
    Amount_Payable NUMBER DEFAULT 0 CHECK (Amount_Payable >= 0),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

-- Administrators table
CREATE TABLE Administrators (
    Admin_ID NUMBER PRIMARY KEY,
    User_ID NUMBER UNIQUE,
    Role VARCHAR2(100) NOT NULL,
    Permissions VARCHAR2(255),
    Last_Login DATE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

-- Authors table
CREATE TABLE Authors (
    Author_ID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Biography CLOB,
    Date_of_Birth DATE,
    Date_of_Death DATE,
    Nationality VARCHAR2(50),
    Languages VARCHAR2(100)
);

-- Genres table
CREATE TABLE Genres (
    Genre_ID NUMBER PRIMARY KEY,
    Title VARCHAR2(50) NOT NULL UNIQUE,
    Description VARCHAR2(255)
);

-- Books table
CREATE TABLE Books (
    ISBN VARCHAR2(20) PRIMARY KEY,
    Title VARCHAR2(200) NOT NULL,
    Publication_Date DATE,
    Pages NUMBER CHECK (Pages > 0),
    Copies_Available NUMBER DEFAULT 1 CHECK (Copies_Available >= 0),
    Publisher VARCHAR2(100),
    Admin_ID NUMBER,
    FOREIGN KEY (Admin_ID) REFERENCES Administrators(Admin_ID)
);

-- BookAuthor table
CREATE TABLE BookAuthor (
    ISBN VARCHAR2(20),
    Author_ID NUMBER,
    PRIMARY KEY (ISBN, Author_ID),
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
    FOREIGN KEY (Author_ID) REFERENCES Authors(Author_ID)
);

-- BookGenre table
CREATE TABLE BookGenre (
    ISBN VARCHAR2(20),
    Genre_ID NUMBER,
    PRIMARY KEY (ISBN, Genre_ID),
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
    FOREIGN KEY (Genre_ID) REFERENCES Genres(Genre_ID)
);

-- Loans table
CREATE TABLE Loans (
    Loan_Number NUMBER PRIMARY KEY,
    Borrower_ID NUMBER,
    ISBN VARCHAR2(20),
    Loan_Date DATE DEFAULT SYSDATE,
    Due_Date DATE,
    Return_Date DATE,
    Fine_Amount NUMBER DEFAULT 0 CHECK (Fine_Amount >= 0),
    Return_Status CHAR(1) CHECK (Return_Status IN ('Y', 'N')),
    Admin_ID NUMBER,
    FOREIGN KEY (Borrower_ID) REFERENCES Borrowers(Borrower_ID),
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
    FOREIGN KEY (Admin_ID) REFERENCES Administrators(Admin_ID)
);
