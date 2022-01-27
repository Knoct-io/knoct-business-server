from celery import shared_task

@shared_task
def send_otp_sms(mobile, otp):
    print("Generating mobile otp")
    pass

@shared_task
def send_otp_mail(email, otp):
    print("Generating mail otp")
    pass