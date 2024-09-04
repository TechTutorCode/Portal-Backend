from mailersend import emails
# Initialize MailerSend
mailer = emails.NewEmail('mlsn.038d33306b90e885edd6ca678ee1f4e1fcfccd3ee4aae95634f817877e8779f9')
def sendVerifyEmail():
    mail_body = {}

    mail_from = {
    "email": "programmingtutor.ke@gmail.com"
    }

    recipients = [
    {
        "email": "dennismwangi4567@gmail.com"
    }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("Hello!", mail_body)
    mailer.set_html_content("Hello, this is an example email from MailerSend", mail_body)
    return mailer.send(mail_body)


res=sendVerifyEmail()
print(res)