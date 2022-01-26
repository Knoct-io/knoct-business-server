from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from .models import Enterprise, User, EmailOtpLogs
from .user_helpers import process_email_otp, process_mobile_otp

class AddEnterpriseView(APIView):
    def post(self, request):
        registration_number = request.data.get('registration_number')
        name = request.data.get('name')
        email = request.data.get('email')
        sector = request.data.get('sector', None)

        if not registration_number or not name or not email:
            return Response({"Success":False, "Message":"Invalid name or mobile or source"}, status=HTTP_400_BAD_REQUEST)

        if Enterprise.objects.get(registration_number=registration_number).exists():
            return Response({"Success":True, "Message":"Enterprise Already Exists"}, status=HTTP_200_OK)
        else:
            process_email_otp(email)
            Enterprise.objects.create(registration_number=registration_number, name=name, email=email, sector=sector)
            return Response({"Success":True, "Message":"User Registered Successfully"}, status=HTTP_200_OK)


class UserSignUpView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        mobile = request.data.get('mobile')
        city_id = request.data.get('city')
        privilege_id = request.data.get('privilege_id')
        enterprise_id = request.data.get('enterprise_id')

        if not name or not email or not mobile:
            return Response({"Success":False, "Message":"Invalid name or mobile or email"}, status=HTTP_400_BAD_REQUEST)

        if User.models.get(email=email, mobile=mobile).exists():
            return Response({"Success":True, "Message":"User Already Exists"}, status=HTTP_200_OK)
        else:
            if not is_otp_verified:
                process_mobile_otp(mobile)
                process_email_otp(email)
            User.objects.create(name=name, email=email, mobile=mobile, city_id=city_id, privilege_id=privilege_id, 
            enterprise_id=enterprise_id)
            return Response({"Success":True, "Message":"User Registered Successfully"}, status=HTTP_200_OK)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        mobile = request.data.get('mobile')
        is_otp_verified = request.data.get('is_otp_verified')

        if not email or not mobile:
            return Response({"Success":False, "Message":"Invalid mobile or email"}, status=HTTP_400_BAD_REQUEST)

        user_qs = User.models.get(email=email, mobile=mobile)
        if not user_qs.exists():
            return Response({"Success":True, "Message":"User Does not Exists"}, status=HTTP_200_OK)
        
        if not is_otp_verified:
            process_mobile_otp(mobile)
            process_email_otp(email)
            return Response({"Success":True, "OTP":"OTP Sent Successfully"}, status=HTTP_200_OK)
        
        user_qs.update(last_logged_in_time=timezone.now)
        return Response({"Success":True, "Message":"User Loggedin Successfully"}, status=HTTP_200_OK)


class VerifyOtpView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')
        if not email or not otp:
            return Response({"Success":False, "Message":"Invalid otp or email"}, status=HTTP_400_BAD_REQUEST)

        email_otp_obj = EmailOtpLogs.objects.filter(email=email).first()
        if not email_otp_obj:
            return Response({"Success":False, "Message":"Otp does not exist"}, status=HTTP_401_UNAUTHORIZED)
        
        if email_otp_obj.otp == otp:
            return Response({"Success":True, "Message":"User Authenticated"}, status=HTTP_200_OK)

        return Response({"Success":False, "Message":"Otp does not exist"}, status=HTTP_401_UNAUTHORIZED)


