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

        