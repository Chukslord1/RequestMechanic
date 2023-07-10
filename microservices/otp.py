from django.core.mail import send_mail
from django.conf import settings
from pyotp import TOTP
import time

otp_secret_key = "base32secret3232"
otp_interval = 300
otp_expiry = 600  # OTP expires after 10 minutes


def generate_otp(email, subject):
    otp = TOTP(otp_secret_key, interval=otp_interval)
    generated_otp = otp.now()
    expiry_time = int(time.time()) + otp_expiry
    otp_string = f"{generated_otp}-{expiry_time}-{email}"
    send_mail(
        subject=f"OTP for {subject}",
        message=f"Your OTP for {subject} is {generated_otp}. It is valid for 10 minutes.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return otp_string


def verify_otp(otp_code, email):
    otp = TOTP(otp_secret_key, interval=otp_interval)
    current_time = int(time.time())

    for otp_attempt in range(current_time, current_time - otp_expiry, -otp_interval):
        expected_otp = otp.at(otp_attempt)
        expected_otp_string = f"{expected_otp}-{otp_attempt}-{email}"
        print(f"Expected OTP string: {expected_otp_string}")
        print(f"Actual OTP string: {otp_code}")

        if otp_code == expected_otp:
            return True

    return False
