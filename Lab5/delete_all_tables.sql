-- Script to drop all tables created in the library database schema
-- Drops tables in reverse order to avoid foreign key constraint issues

-- Drop BookGenre table
DROP TABLE TSELCUK.BookGenre CASCADE CONSTRAINTS;

-- Drop BookAuthor table
DROP TABLE TSELCUK.BookAuthor CASCADE CONSTRAINTS;

-- Drop Loans table
DROP TABLE TSELCUK.Loans CASCADE CONSTRAINTS;

-- Drop Books table
DROP TABLE TSELCUK.Books CASCADE CONSTRAINTS;

-- Drop Genres table
DROP TABLE TSELCUK.Genres CASCADE CONSTRAINTS;

-- Drop Authors table
DROP TABLE TSELCUK.Authors CASCADE CONSTRAINTS;

-- Drop Administrators table
DROP TABLE TSELCUK.Administrators CASCADE CONSTRAINTS;

-- Drop Borrowers table
DROP TABLE TSELCUK.Borrowers CASCADE CONSTRAINTS;

-- Drop Users table
DROP TABLE TSELCUK.Users CASCADE CONSTRAINTS;
