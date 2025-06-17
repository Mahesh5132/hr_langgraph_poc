import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "your_email_password"

def send_email(recipient, subject, body):
    msg = MIMEText(body)
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
    server.quit()

def notify_employee(email, message):
    send_email(email, "Appraisal Notification", message)

def notify_manager(email, message):
    send_email(email, "Action Required: Appraisal Feedback", message)
