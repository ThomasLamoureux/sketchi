import configparser
import secrets
import smtplib
from email.message import EmailMessage

import Database.database as database

config_file = 'Config_Files/email_config.ini'
config = configparser.ConfigParser()
config.read(config_file)

verification_enabled = config.getboolean('email', 'verification_enabled', fallback=True)


debug_mode = True


async def send_verification_email(to_email, verification_code):

    if debug_mode:
        print(f"(Debug Mode) Sending verification code {verification_code} to {to_email}")
        return
    print(f"Sending {verification_code} to {to_email}")
    server_email = config.get('email', 'server_email')
    server_password = config.get('email', 'server_password')

    msg = EmailMessage()
    msg['Subject'] = 'Sketchi Email Verification'
    msg['From'] = server_email
    msg['To'] = to_email
    msg.set_content(f'Your Sketchi verification code is: {verification_code}')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(server_email, server_password)
            server.sendmail(server_email, to_email, msg.as_string())

        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}") 


def generate_verification_code():
    verification_code = secrets.token_hex(3).upper()

    return verification_code


def check_verification_enabled():
    return verification_enabled


def verification_attempt(username, code):
    stored_code = database.get_data_from_account(username, "Email_Verification_Code")

    if stored_code == code:
        database.set_data_in_account(username, "Email_Verified", True)
        return True
    else:
        return False