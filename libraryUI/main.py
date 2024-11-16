import oracledb
from getpass import getpass


try:
    # Prompt user for connection details
    username = input("Enter your database username: ")
    password = getpass("Enter your database password: ")
    
    # Static connection details
    host = "oracle12c.scs.ryerson.ca"
    port = 1521
    sid = "orcl12c"

    # Connection string (DSN)
    dsn = oracledb.makedsn(host, port, sid=sid)

    # Establishing the connection
    conn = oracledb.connect(user=username, password=password, dsn=dsn)
    print("Connection established:", conn.version)

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # Query the Administrators table
    cursor.execute("SELECT * FROM Administrators")

    # Fetch and display the rows
    print("Results from the 'Administrators' table:")
    for row in cursor:
        print(row)

except oracledb.DatabaseError as e:
    # Print database connection errors
    print("Database connection error:", e)
finally:
    # Close the cursor and connection
    if 'cursor' in locals() and cursor:
        cursor.close()
        print("Cursor closed.")
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
