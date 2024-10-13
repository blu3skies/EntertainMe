from dotenv import load_dotenv
import pymysql
import os
import pytest
from quiz import Quiz
from user import User

# Load environment variables for tests
load_dotenv('.env.test')

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


print(f"DB_HOST: {db_host}, DB_USER: {db_user}, DB_PASSWORD: {db_password}, DB_NAME: {db_name}")

@pytest.fixture
def db_connection():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=3306,
        ssl_disabled = True

    )
    cursor = connection.cursor()
    
    # Start a transaction for each test
    connection.begin()

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
        on_watchlist BOOLEAN DEFAULT FALSE,
        unwatched BOOLEAN DEFAULT FALSE,
        quiz_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    );
    ''')

    yield connection, cursor

    # Rollback the transaction after each test to avoid persisting data
    connection.rollback()
    cursor.close()
    connection.close()

def test_user_can_get_watchlist():
    user8 = User("test", "testy", "test8@gmail.com", "!!password!01")
    quiz8 = Quiz(user8.id)

    film81 = quiz8.current_movie_id
    quiz8.add_to_watchlist()
    quiz8.give_score(9)
    film82 = quiz8.current_movie_id
    quiz8.add_to_watchlist()
    user8.return_watchlist()

    assert user8.watchlist == [film81, film82] 

