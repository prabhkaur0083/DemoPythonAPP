from django.core.mail import send_mail
from django.conf import settings


def send_mail_page():
    print("funtiona")
    context = {}

    address = "prabhjot0083@gmail.com"
    subject = "mail-test"
    
    message = "test-message"

    if address and subject and message:
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
            context["result"] = "Email sent successfully"
        except Exception as e:
            context["result"] = f"Error sending email: {e}"
            print(e)
    else:
        context["result"] = "All fields are required"
    print(context)

    return "done"
