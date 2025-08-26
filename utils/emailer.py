import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()
EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_PORT=int(os.getenv("EMAIL_PORT",587))
EMAIL_USER=os.getenv("EMAIL_USER")
EMAIL_PASS=os.getenv("EMAIL_PASS")
ALERT_TO=os.getenv("ALERT_TO")
print("DEBUG Email_User",os.getenv("EMAIL_USER"))
print("DEBUG ALERT_TO",os.getenv("ALERT_TO"))
def send_email_alert(subject,html_body,text_body=None,to=None):
    recipient=to or ALERT_TO
    if not recipient:
        print("No recipent configured")
        return False
    
    try:
        msg=MIMEMultipart("alternative")
        msg["from"]=EMAIL_USER
        msg["To"]=recipient
        msg["Subject"]=subject

        if text_body:
            msg.attach(MIMEText(text_body,"plain"))
            msg.attach(MIMEText(html_body,"html"))

            with smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)as server:
                server.starttls()
                server.login(EMAIL_USER,EMAIL_PASS)
                server.send_message(msg)


                print(f"Email sent To {recipient}")
                return True
    except Exception as e:
        print(f"Failed to send email:{e}")
        return False
    

if __name__=="__main__":
    ok=send_email_alert(subject="Phishgaurd Test Alert ",text_body="this is a plain text test",html_body="<h3>PhishGaurd AI Test</h3><p>This email confirms alerts work </p>")
    print("Email Sent Status",ok)

