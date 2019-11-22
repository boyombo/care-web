from post_office import mail


def send_welcome_email(to_email, name):
    mail.send(
        [to_email],
        "noreply@futurecare.ng",
        template="welcome_email",
        context={"name": name, "username": to_email},
    )


def send_reset_mail(to_email, name, reset_link):
    mail.send(
        [to_email],
        "noreply@futurecare.ng",
        template="reset_email",
        context={"name": name, "reset_link": reset_link},
    )
