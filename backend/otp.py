import smtplib
import random
import time
from email.message import EmailMessage

# Configuration
SENDER_EMAIL = "codebloodedhackon@gmail.com"
SENDER_PASSWORD = "fzlk fnvx undg rcti"  # NOT your Gmail password. Use App Password.

otp_store = {}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp,
        "created_at": time.time()
    }
    print(f" OTP stored for {email}: {otp_store[email]}")

    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg.set_content(f"Your OTP is: {otp}. It will expire in 5 minutes.")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True, "OTP sent successfully"
    except Exception as e:
        return False, f"Failed to send OTP: {e}"

def verify_otp(email, input_otp):
    print(f"Verifying OTP for {email}: got {input_otp}")
    if email not in otp_store:
        print(" Email not found in OTP store!")
    else:
        print(f"Stored OTP: {otp_store[email]['otp']}")

    if email not in otp_store:
        return False, "No OTP sent to this email"

    data = otp_store[email]
    if time.time() - data["created_at"] > 300:
        del otp_store[email]
        return False, "OTP expired"

    if input_otp == data["otp"]:
        del otp_store[email]
        return True, "OTP verified!"
    return False, "Incorrect OTP"
