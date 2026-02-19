from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS
            msg['Subject'] = "New Contact Form Message"

            body = f"""
            New message received:

            Name: {name}
            Email: {email}
            Message: {message}
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            flash("Message sent successfully!", "success")

        except Exception as e:
            print("Error:", e)
            flash("Something went wrong. Try again.", "danger")

        return redirect(url_for('home') + '#contact')

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)