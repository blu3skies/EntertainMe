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
        fname VARCHAR(50) NOT NULL,
        lname VARCHAR(50),
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
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
        elif self.user_exists(email):
            raise ValueError ("Account already exists, please sign in with this email address.")
        elif password == "":
            raise ValueError ("Password is required")
        elif not self.password_is_strong(password):
            raise ValueError ("Password is not strong")
        else:
            self.fname = fname
            self.lname = lname 
            self.email = email
            self.password = password
            self._create_user_in_db()
            self.id = self.giveid(email)
    
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
    
    def user_exists(self, email):
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute('SELECT email FROM users WHERE email = %s', (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        # If a result is found, the user exists, return True
        if result:
            return True
        else:
            return False

        

    def _create_user_in_db(self):
        # Re-establish the database connection
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )

        cursor = connection.cursor()    

        try:
            # Insert the user into the database
            cursor.execute('''
                           INSERT INTO users (fname, lname, password_hash, email)
                           VALUES (%s, %s, %s, %s)
                           ''', (self.fname, self.lname, self.password, self.email))
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    def giveid(self, email):
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306
        )

        cursor = connection.cursor()
        cursor.execute('SELECT user_id FROM users WHERE email = %s', (email,))
        result = cursor.fetchone()
        return result[0]


#try:
#    user1 = User("John", "Doe", "john.doe1@example.com", "Ronni3i!s3pic")
#    user1 = User("John", "Doe", "john.doe2@exampg=le.com", "Ronni3!is3pic")
#except ValueError as e:
#    print(f"Error: {e}")