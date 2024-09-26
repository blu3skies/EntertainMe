from user import User
import pytest

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