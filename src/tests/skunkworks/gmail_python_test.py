import os
import smtplib
import ssl
from email.message import EmailMessage

# 1. Configuration
# Use your main Gmail address as the username
GMAIL_USER=os.environ.get("GMAIL_USER")                     # 'rnemzek@gmail.com' 
# Use the 16-character App Password you just generated (no spaces)
GMAIL_APP_PASSWORD=os.environ.get("GMAIL_APP_PASSWORD")     # 'ioetj lnib pety yttt'

# 2. Set the recipient with your custom plus-tag alias
RECIPIENT_EMAIL = 'rnemzek+python@gmail.com'

# 3. Create the email content
msg = EmailMessage()
msg['Subject'] = 'Python Automation Test'
msg['From'] = GMAIL_USER
msg['To'] = RECIPIENT_EMAIL
msg.set_content('This is a test email sent from Python to a Gmail alias!')

# 4. Send the email securely
context = ssl.create_default_context()

try:
    # Connect to Gmail's SMTP server using SSL on port 465
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
    print(f"Success! Email sent to {RECIPIENT_EMAIL}")
except Exception as e:
    print(f"Error: {e}")

