import pytest
from flask import url_for

@pytest.fixture
def client(app):
    # The 'client' fixture provided by pytest-flask
    return app.test_client()

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
    login_url = url_for('signin')
    login_data = {
        'email': 'testuser1@example.com',
        'password': 'securepassword01!'
    }
    response = client.post(login_url, data=login_data, follow_redirects=True)
    assert response.status_code == 200  # Ensure login succeeded

    assert b'testuser1@example.com' in response.data  # Assuming some quiz text is rendered on the page


    # Step 4: Assert that the 'Start Quiz' button is on the page
    # Assuming the button is part of the page after login
    assert b'Start Quiz' in response.data  # Check that the button text is in the HTML
    response = client.get(url_for('start_quiz'), follow_redirects=True)
    assert response.status_code == 200  
    assert b'testuser1@example.com' in response.data  # Assuming some quiz text is rendered on the page
    assert b'Rate the Movie' in response.data  # Assuming some quiz text is rendered on the page


def test_signout(client):
    login_url = url_for('signin')
    login_data = {
        'email': 'testuser1@example.com',
        'password': 'securepassword01!'
    }
    response = client.post(login_url, data=login_data, follow_redirects=True)
    assert response.status_code == 200

    signout_url = url_for('signout')
    
    # Use GET request to sign out
    response = client.get(signout_url, follow_redirects=True)
    assert response.status_code == 200
