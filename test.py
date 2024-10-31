import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    sender_email = "ahmedezzat@nedialo.com"
    sender_password = "password"  # App-specific password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Upgrade connection to TLS
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")




# Usage
send_email("Test Subject", "This is the body of the email", "ahmedezzat@nedialo.com")
