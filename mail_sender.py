# -*- coding: utf-8 -*-
from flask_mail import Mail, Message

def send_mail(app, recipient, new_password):
    mail = Mail(app)
    msg = Message("Nowe hasło",
                sender=app.config["MAIL_USERNAME"],
                recipients=[recipient])
    msg.body = "Twoje nowe hasło to: " + new_password

    mail.send(msg)