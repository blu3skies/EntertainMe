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
    cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
    cursor.execute('DROP TABLE IF EXISTS quiz_results')
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        fname VARCHAR(50) NOT NULL,
        lname VARCHAR(50),
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
        );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        quiz_result_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        score INT CHECK (score BETWEEN 1 AND 10),
        quiz_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
        );      
    ''')
    
    yield connection, cursor  # Provide the connection and cursor to the test
    cursor.close()
    connection.close()
    
    yield connection, cursor  # Provide the connection and cursor to the test
    cursor.close()
    connection.close()

def test_an_create_new_user():
    testuser = User("Joe", "Elling", "jelling0@gmail.com", "password!01")
    assert testuser.fname == "Joe"
    assert testuser.lname == "Elling"
    assert testuser.email == "jelling0@gmail.com"
    assert testuser.password =="password!01"

def test_fname_and_email_and_password_are_not_empty():
    with pytest.raises(ValueError, match="First name is required"):
        user1 = User("", "Elling", "jelling1@gmail.com", "password!01")
    with pytest.raises(ValueError, match="Email address is required"):
        user2 = User("Joe", "Elling", "", "password!01")
    with pytest.raises(ValueError, match="Password is required"):
        user3 = User("Joe", "Elling", "jelling3@gmail.com", "")

def test_email_is_valid():
    with pytest.raises(ValueError, match="A valid email is required"):
        user4 = User("Joe", "Elling", "joeemail.com", "password!01")
    with pytest.raises(ValueError, match="A valid email is required"):
        user5 = User("Joe", "Elling", "joe21@emailcom", "password!01")

def test_password_is_strong():
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        user6 = User("Joe", "Elling", "joe@email.com", "pas!1")
    with pytest.raises(ValueError, match="Password must contain at least one symbol"):
        user7 = User("Joe", "Elling", "joe@email.com", "Passwordwithoutsymbol1")
    with pytest.raises(ValueError, match="Password must contain at least one number"):
        user8 = User("Joe", "Elling", "joe@email.com", "Passwordwithoutnumber!")

def test_user_already_exists():
    peppa1 = User("Peppa1", "Elling", "peppa1@hotmail.com", "Snacks!21")
    with pytest.raises(ValueError, match="Account already exists, please sign in with this email address."):
        peppa2 = User("Peppa2", "el", "peppa1@hotmail.com", "Ronni3is3pic!")



    