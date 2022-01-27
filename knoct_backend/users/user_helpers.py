from random import randrange
from django.utils import timezone

from .constants import MIN_OTP_VALUE, MAX_OTP_VALUE
from .models import MobileOtpLogs, EmailOtpLogs
from .tasks import send_otp_sms, send_otp_mail

def generate_otp():
    return randrange(MIN_OTP_VALUE, MAX_OTP_VALUE + 1)


def process_mobile_otp(mobile):
    otp = generate_otp()
    MobileOtpLogs.objects.create(mobile=mobile, otp=otp)
    send_otp_sms(mobile, otp)
    return otp


def process_email_otp(email):
    otp = generate_otp()
    EmailOtpLogs.objects.create(email=email, otp=otp)
    send_otp_mail(email, otp)
    return otp

def time_validated_in_seconds(created_at, valid_time):
    print((timezone.now()-created_at).seconds)
    print(valid_time)
    return (timezone.now()-created_at).seconds<valid_time
