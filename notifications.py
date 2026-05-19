import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit


# =========================
# EMAIL FUNCTION
# =========================
def send_email(to_email: str, subject: str, message: str) -> bool:
    sender_email = "vivektiwari88810@gmail.com"
    app_password = "nastcmeokjosmuxo"  # ⚠️ move to env in real project

    try:
        # Create email message
        msg = MIMEText(message, "plain")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # secure connection
            server.login(sender_email, app_password)
            server.send_message(msg)

        print("✅ Email sent successfully")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed: check email/app password")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error occurred: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return False


# =========================
# WHATSAPP FUNCTION
# =========================
def send_whatsapp(phone_number: str, message: str) -> bool:
    try:
        phone_number = phone_number.strip()

        kit.sendwhatmsg_instantly(
            phone_number,
            message,
            wait_time=15,
            tab_close=True
        )

        print("✅ WhatsApp message sent")
        return True

    except Exception as e:
        print(f"❌ WhatsApp failed: {e}")
        return False