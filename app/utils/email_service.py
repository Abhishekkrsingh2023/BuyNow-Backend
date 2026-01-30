from aiosmtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.settings import settings

def return_otp_email_html(username: str, otp: str) -> str:
    HTML_TEMPLATE = f''' 
<!DOCTYPE html>
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
    <div style="max-width: 480px; margin: auto; background: #ffffff; padding: 20px; border-radius: 6px;">

      <h2 style="color: #333; text-align: center;"><b>BuyNow</b> - Email Verification</h2>

      <p>Hello {username},</p>

      <p>Your One-Time Password (OTP) for email verification is:</p>

      <div style="text-align: center; margin: 20px 0;">
        <span style="
          display: inline-block;
          padding: 12px 20px;
          background: #1a73e8;
          color: #fff;
          font-size: 24px;
          font-weight: bold;
          border-radius: 4px;">
          {otp}
        </span>
      </div>

      <p>This OTP is valid for 10 minutes. Do not share it with anyone.</p>

      <p>If you did not request this, you may ignore the email.</p>

      <p style="margin-top: 30px;">Regards,<br><b>BuyNow</b> Team</p>

    </div>
  </body>
</html>
'''
    return HTML_TEMPLATE


async def send_message_dependency(receiver: dict, otp: str) -> dict:
    """
    send_message_dependency
    
    :param receiver: A dictionary containing the receiver's details, including 'email' and 'name'
    :type receiver: dict
    :param otp: The one-time password to be sent in the email
    :type otp: str
    :return: A dictionary indicating the result of the email sending operation
    :rtype: dict 
    """
    message = MIMEMultipart()
    message["Subject"] = "Email Verification - Your OTP Code"
    message["From"] = settings.SENDERS_EMAIL
    message["To"] = receiver["email"]
    message["Reply-To"] = settings.SENDERS_EMAIL

    html_message = return_otp_email_html(receiver["name"], otp)
    message.attach(MIMEText(html_message, "html"))

    smtp = SMTP(hostname="smtp.gmail.com", port=587, start_tls=True)

    try:
        await smtp.connect()
        await smtp.login(settings.SENDERS_EMAIL, settings.GMAIL_PASSWORD)
        await smtp.sendmail(settings.SENDERS_EMAIL, [receiver["email"]], message.as_string())
        return {"message": "sent successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    finally:
        try:
            await smtp.quit()
        except:
            pass
