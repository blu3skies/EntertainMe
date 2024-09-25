class User:
    __fname = ""
    __lname = ""
    __email = ""
    __password = ""

    def __init__(self, fname, lname, email, password):

        if fname == "":
            raise ValueError ("First name is required")
        elif email == "":
            raise ValueError ("Email address is required")
        elif not self.valid_email_check(email):
            raise ValueError ("A valid email is required")
        elif password == "":
            raise ValueError ("Password is required")
        elif not self.password_is_strong(password):
            raise ValueError ("Password is not strong")
        else:
            self.fname = fname
            self.lname = lname 
            self.email = email
            self.password = password
    
    def valid_email_check(self, email):
        return '@' in email and '.' in email
    
    def password_is_strong(self, password):
        specialChars = ['?', '£', '%', '&', '$', '#', '@', '!', '*']
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif not any(char in password for char in specialChars):
            raise ValueError("Password must contain at least one symbol")
        elif not any(chr.isdigit() for chr in password):
            raise ValueError("Password must contain at least one number")
        return True  # Only return True if all checks pass

        
# Troubleshooting block
try:
    user = User("John", "Doe", "john.doe@example.com", "wkjlfdksffssfds!ass")
except ValueError as e:
    print(f"Error: {e}")