import pymysql
import os
import pytest
from user import User

# Fetch database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


def test_new_user_in_db():
    # Re-establish the connection and cursor for this test
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=3306
    )
    cursor = connection.cursor()

    # Create a new user
    peppa = User("Peppa", "Elling", "peppa@hotmail.com", "Snacks!21")
    
    # Correct the SQL query with %s for parameter
    cursor.execute('SELECT fname FROM users WHERE email = %s', (peppa.email,))
    result = cursor.fetchone()

    # Assert that the first name of the user matches
    assert result[0] == "Peppa"

    # Close the cursor and connection
    cursor.close()
    connection.close()