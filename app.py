from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/send-email", methods=['POST'])
def send_email():
    smtp_server = request.form.get('smtp_server')
    smtp_port = request.form.get('smtp_port')
    sender_email = request.form.get('sender_email')
    sender_password = request.form.get('sender_password')
    subject = request.form.get('subject')
    message = request.form.get('message')
    recipients = request.form.get('recipients')
    file = request.files.get('attachment')

    recipients = recipients.split(',')

    try:
        smtp_port = int(smtp_port)
    except ValueError:
        return 'SMTP port must be a number'

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['Subject'] = subject
        msg['To'] = ', '.join(recipients)

        msg.attach(MIMEText(message, 'html'))

        if file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={file.filename}')
            msg.attach(attachment)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        server.send_message(msg)
        server.quit()

        return 'Email sent successfully!'
    except Exception as e:
        return f'Error sending email: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True) 
