class User:
    __fname = ""
    __lname = ""
    __email = ""

    def __init__(self, fname, lname, email):

        if fname == "":
            raise ValueError ("First name is required")
        else:
            self.fname = fname
            self.lname = lname 
            self.email = email


ronnie = User("ron", "Elling", "ronnie@woof.com")
print(ronnie.fname)