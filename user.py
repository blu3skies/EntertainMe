import os
import pymysql

# Fetch database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Establish the connection using environment variables
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=3306  # Default port
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Example: Create a users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        fname VARCHAR(50) UNIQUE, -- NOT NULL
        lname VARCHAR(50) UNIQUE, -- NULL ALLOWED
        password_hash VARCHAR(255),
        email VARCHAR(100) UNIQUE
    );
''')

# Commit the changes to the database
connection.commit()

# Close the connection
cursor.close()
connection.close()


class User:
    __fname = ""
    __lname = ""
    __email = ""
    __password = ""

    def __init__(self, fname, lname, email, password):

        if fname == "":
            raise ValueError ("First name is required")
        elif email == "":
            raise ValueError ("Email address is required")
        elif not self.valid_email_check(email):
            raise ValueError ("A valid email is required")
        elif password == "":
            raise ValueError ("Password is required")
        elif not self.password_is_strong(password):
            raise ValueError ("Password is not strong")
        else:
            self.fname = fname
            self.lname = lname 
            self.email = email
            self.password = password
    
    def valid_email_check(self, email):
        return '@' in email and '.' in email
    
    def password_is_strong(self, password):
        specialChars = ['?', '£', '%', '&', '$', '#', '@', '!', '*']
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif not any(char in password for char in specialChars):
            raise ValueError("Password must contain at least one symbol")
        elif not any(chr.isdigit() for chr in password):
            raise ValueError("Password must contain at least one number")
        return True  # Only return True if all checks pass

        
