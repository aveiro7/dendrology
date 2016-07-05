from flask_mail import Mail, Message

def send_mail(app, recipient, new_password):
    mail = Mail(app)
    msg = Message("Nowe haslo",
                sender=app.config["MAIL_USERNAME"],
                recipients=[recipient])
    msg.body = "Twoje nowe haslo to: " + new_password

    mail.send(msg)