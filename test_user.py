from user import User
import pytest

def test_an_create_new_user():
    testuser = User("Joe", "Elling", "jelling@gmail.com")

    assert testuser.fname == "Joe"
    assert testuser.lname == "Elling"
    assert testuser.email == "jelling@gmail.com"


