import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from settings import EMAIL_USER, EMAIL_PASS, SMTP_HOST, SMTP_PORT

# TARGET EMAIL (Boss)
EMAIL_TO = "nrveeresh327@gmail.com"

def send_report_email(summary_pdf, invoice_pdf, approval_token):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = "JRAVIS Daily Report – Approval Required"

    body = f"""
Boss,

Your daily report is ready.

Approval Code: {approval_token}

Regards,
JRAVIS
"""
    msg.attach(MIMEText(body, "plain"))

    for file_path in [summary_pdf, invoice_pdf]:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(file_path, "rb").read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename={file_path}")
        msg.attach(part)

    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp.starttls()
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
    smtp.quit()

    print("✔ Email sent to Boss:", EMAIL_TO)
