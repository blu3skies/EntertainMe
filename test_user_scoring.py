import pymysql
import os
import pytest
from quiz import Quiz
from user import User

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

def test_user_can_start_a_quiz():

    user1 = User("test", "testy", "test1@gmail.com", "!!password!01")
    quiz1 = Quiz(user1.id)

    assert quiz1.user_id == 3

def test_quiz_presents_movie():
    user2 = User("test", "testy", "test2@gmail.com", "!!password!01")
    quiz2 = Quiz(user2.id)

    assert quiz2.current_movie_id is not None



def test_user_can_give_movie_a_score(db_connection):
    connection, cursor = db_connection
    user3 = User("test", "testy", "test3@gmail.com", "!!password!01")
    quiz3 = Quiz(user3.id)

    quiz3.give_score(9)

    cursor.execute('SELECT score FROM quiz_results WHERE user_id = %s', (user3.id,))
    result = cursor.fetchone()

    # Assert that the first name of the user matches
    assert result[0] == 9


    
    
