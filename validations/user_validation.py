from exceptions import mycustomexception
class validations:
    def check_email_entry(self,email):
        if email == " ":
            return mycustomexception("Please enter an email address")

        if "mail.com" not in email["email"]:
            return mycustomexception("Invalid email")

        if "@" not in email["email"] or "." not in email["email"]:
            return mycustomexception("Invalid email")
