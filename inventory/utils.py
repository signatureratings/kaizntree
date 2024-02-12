import bcrypt
from django.core.mail import send_mail

def hash_token(token):
    try:
        hashed_token = bcrypt.hashpw(token.encode(), bcrypt.gensalt())
        return hashed_token.decode()
    except Exception as e:
        print(f"Error occurred while converting password to hash: {str(e)}")
        raise e

def verify_token(token, hashed_token):
    try:
        result = bcrypt.checkpw(token.encode(), hashed_token.encode())
        return result
    except Exception as e:
        print(f"Error occurred while converting hash to password: {str(e)}")
        raise e
    
def send_email(subject, message, from_email, recipient_list):
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        print(f"Error occurred while sending email: {str(e)}")
        return False
    