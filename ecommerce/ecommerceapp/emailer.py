from . import views,emailer2
import smtplib

from email.message import EmailMessage



from_email = emailer2.user
password = emailer2.password

def send_verify_email(message,email,subject="Tonworld"):
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com',587)
        smtp_object.ehlo()
        smtp_object.starttls()
        smtp_object.login(from_email,password)

        full_message = f"Subject: {subject}\n\n{message}"

        smtp_object.sendmail(from_email, email, full_message)
        print("successful")
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False
    finally:
        smtp_object.quit() 