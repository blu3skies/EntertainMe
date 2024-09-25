from user import User
import pytest

def test_an_create_new_user():
    testuser = User("Joe", "Elling", "jelling@gmail.com")
    assert testuser.fname == "Joe"
    assert testuser.lname == "Elling"
    assert testuser.email == "jelling@gmail.com"

def test_fname_and_email_are_not_empty():
    with pytest.raises(ValueError, match="First name is required"):
        user1 = User("", "Elling", "jelling@gmail.com")
    with pytest.raises(ValueError, match="Email address is required"):
        user2 = User("Joe", "Elling", "")

def test_email_is_valid():
    with pytest.raises(ValueError, match="A valid email is required"):
        user3 = User("Joe", "Elling", "joeemail.com")
    with pytest.raises(ValueError, match="A valid email is required"):
        user4 = User("Joe", "Elling", "joe@emailcom")