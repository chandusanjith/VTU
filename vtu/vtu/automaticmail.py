from django.template.loader import render_to_string, get_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .models import EmailConfig

def SendEmail(reciever_mail, context ,subject , format_html):
    mail_html = get_template(format_html).render(context)
    # The mail addresses and password
    sender = EmailConfig.objects.filter(id=1).first()
    sender_address = sender.email_id
    sender_pass = sender.password
    receiver_address = reciever_mail
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_html, 'html'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return True