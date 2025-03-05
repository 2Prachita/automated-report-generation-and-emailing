from datetime import datetime
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
SENDER = os.getenv('SENDER')
RECEIVER = os.getenv('RECEIVER')
PASSWORD = os.getenv('PASSWORD')

def daily_sale_report_email(date: datetime):
    # Sender and Receiver Email
    sender_email = SENDER
    receiver_email = RECEIVER
    password = PASSWORD

    # Setup the MIME
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Sales Report for {date: %d %B %Y}"

    # 📌 Email Body (HTML Format Allowed)
    email_body = f"""
    Hello Team,<br><br>

    Please find the attached sales report for this date {date: %Y-%m-%d}.<br>

    Best Regards,<br>
    PK
    """
    message.set_content("This is a plain text version of the email.")  # Plain text fallback
    message.add_alternative(email_body, subtype="html")  # HTML body

    file_path = f'reports/Sales Report {date: %Y-%m-%d}.pdf'  # Change this to the file you want to attach
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        file_data = file.read()
        file_type = "application/pdf"  # Change based on file type (e.g., image/png, text/plain)
        message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)



    # SMTP Server Configuration
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return("Email sent successfully!")
    except Exception as e:
        return(f"Error: {e}")