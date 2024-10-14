import pytest
from dotenv import load_dotenv
from flask import url_for
import pymysql
import os
from quiz import Quiz
from user import User

load_dotenv('.env.test')

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

@pytest.fixture
def client(app):
    # The 'client' fixture provided by pytest-flask
    return app.test_client()

def sign_in_for_test(client):
    login_url = url_for('signin')
    login_data = {
        'email': 'testuser1@example.com',
        'password': 'securepassword01!'
    }
    response = client.post(login_url, data=login_data, follow_redirects=True)
    assert response.status_code == 200

def test_signup_and_login(client):
    # Step 1: Go to the signup page
    signup_url = url_for('signup')
    response = client.get(signup_url)
    assert response.status_code == 200  # Ensure the page loads

    # Step 2: Sign up a new user
    signup_data = {
        'fname': 'Test',
        'lname': 'User',
        'email': 'testuser1@example.com',
        'password': 'securepassword01!'
    }
    response = client.post(signup_url, data=signup_data, follow_redirects=True)
    assert response.status_code == 200  # Check if signup succeeded

    # Step 3: Sign in with the new user credentials
    sign_in_for_test(client)

    # Step 4: After sign-in, navigate to the home page where the user's email should be displayed
    home_url = url_for('home')
    response = client.get(home_url, follow_redirects=True)
    assert response.status_code == 200  # Ensure the home page loads

    # Step 5: Assert that the user's email is on the home page
    assert b'testuser1@example.com' in response.data  # Assuming some quiz text is rendered on the page

    # Step 4: Assert that the 'Start Quiz' button is on the page
    # Assuming the button is part of the page after login
    assert b'Start Quiz' in response.data  # Check that the button text is in the HTML
    response = client.get(url_for('start_quiz'), follow_redirects=True)
    assert response.status_code == 200  
    assert b'testuser1@example.com' in response.data  # Assuming some quiz text is rendered on the page
    assert b'Rate the Movie' in response.data  # Assuming some quiz text is rendered on the page


def test_signout(client):
    sign_in_for_test(client)
    signout_url = url_for('signout')
    
    # Use GET request to sign out
    response = client.get(signout_url, follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data  # Assuming some quiz text is rendered on the page


def test_user_can_end_quiz(client):
    sign_in_for_test(client)
    response = client.get(url_for('start_quiz'), follow_redirects=True)
    assert response.status_code == 200
    response = client.get(url_for('end_quiz'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Start Quiz' in response.data  # Assuming some quiz text is rendered on the page

from unittest.mock import patch

def test_user_can_see_movie_title(client, app):
    with app.app_context():
        # Step 1: Sign in for the test
        sign_in_for_test(client)

        # Step 2: Retrieve user ID from the session or database
        response = client.get(url_for('home'), follow_redirects=True)
        assert response.status_code == 200

        # Assuming you have access to the session data or user data:
        user = User.signin('testuser1@example.com', 'securepassword01!')
        user_id = user.id

        # Step 3: Mock the Quiz.get_movie method to return a specific movie ID
        with patch('quiz.Quiz.get_movie', return_value=597):  # Mock to always return 'Titanic'
            response = client.get(url_for('start_quiz'), follow_redirects=True)
            assert response.status_code == 200

            # Initialize the Quiz object based on the signed-in user's ID
            quiz = Quiz(user_id)
            print(f"Mocked Movie ID in Quiz: {quiz.current_movie_id}")
            print(f"Mocked Movie Title in Quiz: {quiz.current_movie_name}")

            # Debug: Print the HTML response to inspect
            print(response.data.decode())

            # Fetch the movie title from the database using current_movie_id
            connection = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=3306
            )
            cursor = connection.cursor()
            cursor.execute('SELECT title FROM movies WHERE id = %s', (quiz.current_movie_id,))
            movie_title = cursor.fetchone()[0]
            print(f"Movie Title from Database: {movie_title}")
            cursor.close()
            connection.close()

            # Step 4: Check if the movie title is in the HTML response
            assert movie_title.encode() in response.data  # Movie title should appear in the response
            
#def test_user_can_see_their_watchlist(client):
#    login_url = url_for('signin')
#    login_data = {
#        'email': 'testuser1@example.com',
#        'password': 'securepassword01!'
#    }
#    response = client.post(login_url, data=login_data, follow_redirects=True)
#    assert response.status_code == 200
#    response = client.get(url_for('start_quiz'), follow_redirects=True)
#    assert response.status_code == 200
#    response = client.get(url_for('start_quiz'), follow_redirects=True)
