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
        else:
            self.fname = fname
            self.lname = lname 
            self.email = email
            self.password = password
    
    def valid_email_check(self, email):
        return '@' in email and '.' in email


#ronnie = User("ron", "Elling", "ronniewoof.com")
