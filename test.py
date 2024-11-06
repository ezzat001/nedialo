import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = "ahmedezzat@nedialo.com"  # Replace with the sender's email
password = ""  # App password if using 2SV
recipient_email = "recipient@example.com"  # Replace with the recipient's email

smtp_server = "smtp-relay.gmail.com"
smtp_port = 587  # TLS port

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = recipient_email
msg['Subject'] = "Test Email from External User"

msg.attach(MIMEText("This email is sent from an external user!", "plain"))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption
    server.login(email, password)  # Log in
    server.sendmail(email, recipient_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    server.quit()
