class User:
    __fname = ""
    __lname = ""
    __email = ""

    def __init__(self, fname, lname, email):

        if fname == "":
            raise ValueError ("First name is required")
        elif email == "":
            raise ValueError ("Email address is required")
        elif not self.valid_email_check(email):
            raise ValueError ("A valid email is required")
        else:
            self.fname = fname
            self.lname = lname 
            self.email = email
    
    def valid_email_check(self, email):
        return '@' in email and '.' in email


#ronnie = User("ron", "Elling", "ronniewoof.com")
