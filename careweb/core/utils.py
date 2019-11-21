from post_office import mail


def send_welcome_email(to_email, name):
    mail.send(
        [to_email],
        "noreply@futurecare.ng",
        template="welcome_email",
        context={"name": name, "username": to_email},
    )
