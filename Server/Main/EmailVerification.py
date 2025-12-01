import smtplib
from email.message import EmailMessage



def send_verification_email(to_email, verification_code):
    server_email = "dankdomtom@gmail.com"
    server_password = "plit fdlu loxt tlka"

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


send_verification_email("understarlightyoushine@gmail.com", "123456")