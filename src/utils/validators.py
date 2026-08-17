

def validate_age(age):
    if age >= 18:
        return True
    
def validate_email(email):
    if "@" in email and "." in email:
        return True
