import json
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# load config
with open("config.json", "r") as f:
    config = json.load(f)


def send_email(subject, body, to_email, attachment_path):
    # Your Gmail account credentials
    gmail_user = config["email"]
    gmail_password = config["password"]  # If using App Passwords

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, "plain"))

    if attachment_path:
        # Open the file in binary mode
        with open(attachment_path, "rb") as attachment:
            # Create a MIMEBase object
            mime_base = MIMEBase("application", "octet-stream")
            mime_base.set_payload(attachment.read())

            # Encode the attachment in base64
            encoders.encode_base64(mime_base)

            # Add header for the attachment
            mime_base.add_header(
                "Content-Disposition", f"attachment; filename=invoice.pdf"
            )

            # Attach the file to the email
            msg.attach(mime_base)

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_password)

        # Send the email
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


# Usage
# send_email(
#     'Test Subject',
#     'This is the body of the email',
#     'recipient-email@example.com',
#     'path/to/your/file.pdf'
# )
