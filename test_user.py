from user import User
import pytest

def test_an_create_new_user():
    testuser = User("Joe", "Elling", "jelling@gmail.com", "password")
    assert testuser.fname == "Joe"
    assert testuser.lname == "Elling"
    assert testuser.email == "jelling@gmail.com"
    assert testuser.password =="password"

def test_fname_and_email_and_password_are_not_empty():
    with pytest.raises(ValueError, match="First name is required"):
        user1 = User("", "Elling", "jelling@gmail.com", "password")
    with pytest.raises(ValueError, match="Email address is required"):
        user2 = User("Joe", "Elling", "", "password")
    with pytest.raises(ValueError, match="Password is required"):
        user3 = User("Joe", "Elling", "jelling@gmail.com", "")

def test_email_is_valid():
    with pytest.raises(ValueError, match="A valid email is required"):
        user4 = User("Joe", "Elling", "joeemail.com", "password")
    with pytest.raises(ValueError, match="A valid email is required"):
        user5 = User("Joe", "Elling", "joe@emailcom", "password")