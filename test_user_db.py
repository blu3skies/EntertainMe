import pymysql
import os
import pytest
from user import User

# Fetch database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

@pytest.fixture
def db_connection():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=3306
    )
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        fname VARCHAR(50) NOT NULL,
        lname VARCHAR(50),
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
        );
    ''')
    yield connection, cursor  # Provide the connection and cursor to the test
    cursor.close()
    connection.close()


def test_new_user_in_db(db_connection):
    connection, cursor = db_connection
    peppa = User("Peppa", "Elling", "peppa@hotmail.com", "Snacks!21")
    cursor.execute('SELECT fname FROM users WHERE email = %s', (peppa.email,))
    result = cursor.fetchone()

    # Assert that the first name of the user matches
    assert result[0] == "Peppa"

    