from re import T
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                    HTTP_401_UNAUTHORIZED)
from rest_framework.views import APIView
from django.core.cache import cache

from .constants import MAX_OTP_TIME
from .models import EmailOtpLogs, Enterprise, MobileOtpLogs, User, City, Privilege, Sector, Nationality
from .serializers import CitySerializer, PrivilegeSerializer, SectorSerializer, UserSerializer\
    ,NationalitySerializer
from .user_helpers import (process_email_otp, process_mobile_otp,
                            time_validated_in_seconds)


class AddEnterpriseView(APIView):
    def post(self, request):
        registration_number = request.data.get('registration_number')
        name = request.data.get('name')
        email = request.data.get('email')
        sector_id = request.data.get('sector_id')

        if not registration_number or not name or not email or not sector_id:
            return Response({"Success":False, "Message":"Invalid name or mobile or source or sector_id"}, status=HTTP_400_BAD_REQUEST)

        if Enterprise.objects.filter(registration_number=registration_number).exists():
            return Response({"Success":True, "Message":"Enterprise Already Exists"}, status=HTTP_200_OK)
        else:
            process_email_otp(email)
            enterprise_obj = Enterprise.objects.create(registration_number=registration_number, name=name, email=email, sector_id=sector_id)
            return Response({"Success":True, "enterprise_id":enterprise_obj.id, "Message":"Enterprise Added Successfully"}, status=HTTP_200_OK)


class UserSignUpView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        mobile = request.data.get('mobile')
        city_id = request.data.get('city')
        privilege_id = request.data.get('privilege_id')
        enterprise_id = request.data.get('enterprise_id')

        if not name or not email or not mobile or not enterprise_id or not privilege_id:
            return Response({"Success":False, "Message":"Invalid name or mobile or email or enterprise_id, or privilege_id"}, status=HTTP_400_BAD_REQUEST)

        if User.models.filter(email=email, mobile=mobile).exists():
            return Response({"Success":True, "Message":"User Already Exists"}, status=HTTP_200_OK)
        else:
            process_mobile_otp(mobile)
            process_email_otp(email)
            user_obj = User.objects.create(name=name, email=email, mobile=mobile, city_id=city_id, privilege_id=privilege_id, 
            enterprise_id=enterprise_id)
            return Response({"Success":True, "user_id":user_obj.id, "Message":"User Registered Successfully"}, status=HTTP_200_OK)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        mobile = request.data.get('mobile')

        if not email or not mobile:
            return Response({"Success":False, "Message":"Invalid mobile or email"}, status=HTTP_400_BAD_REQUEST)

        user_qs = User.models.get(email=email, mobile=mobile)
        if not user_qs.exists():
            return Response({"Success":True, "Message":"User Does not Exists"}, status=HTTP_200_OK)
        
        process_mobile_otp(mobile)
        process_email_otp(email)
        
        user_qs.update(last_logged_in_time=timezone.now())
        return Response({"Success":True, "Message":"User Loggedin Successfully"}, status=HTTP_200_OK)


class VerifyOtpView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')
        mobile = request.data.get('mobile')
        is_user = request.data.get('is_user')

        if not otp or not email or is_user is None:
            return Response({"Success":False, "Message":"Invalid otp or email or page"}, status=HTTP_400_BAD_REQUEST)

        if mobile:
            mobile_otp_obj = MobileOtpLogs.objects.filter(mobile=mobile).order_by('created_at').first()
            if not mobile_otp_obj:
                return Response({"Success":False, "Message":"Otp does not exist"}, status=HTTP_401_UNAUTHORIZED)
            
            if mobile_otp_obj.otp == otp and time_validated_in_seconds(mobile_otp_obj.created_at, MAX_OTP_TIME):
                try:
                    user = User.objects.get(mobile=mobile)
                    user.mobile_verified=1
                    user.save()
                    return Response({"Success":True, "Message":"Mobile Authenticated"}, status=HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"Success":False, "Message":"Unknown User"}, status=HTTP_400_BAD_REQUEST)

        if email:
            email_otp_obj = EmailOtpLogs.objects.filter(email=email).order_by('-created_at').first()
            if not email_otp_obj:
                return Response({"Success":False, "Message":"Otp Expired"}, status=HTTP_401_UNAUTHORIZED)

            if email_otp_obj.otp == otp and time_validated_in_seconds(email_otp_obj.created_at, MAX_OTP_TIME):
                try:
                    if is_user:
                        user = User.objects.get(email=email).email_verified=1
                        user.email_verified=1
                        user.save()
                        return Response({"Success":True, "Message":"User Email Authenticated"}, status=HTTP_200_OK)
                    enterprise = Enterprise.objects.get(email=email)
                    enterprise.is_verified=1
                    enterprise.save()
                except User.DoesNotExist or Enterprise.DoesNotExist:
                    return Response({"Success":True, "Message":"Email Unknown"}, status=HTTP_200_OK)

        return Response({"Success":False, "Message":"Otp does not exist"}, status=HTTP_401_UNAUTHORIZED)


class SiteConfigView(APIView):
    def get(self, request, *args, **kwargs):
        CitySerializer, PrivilegeSerializer, SectorSerializer
        process_mobile_otp()
        process_email_otp()
        data = {
            "city": CitySerializer(City.objects.all(), many=True).data,
            "privilege": PrivilegeSerializer(Privilege.objects.all(), many=True).data,
            "sector": SectorSerializer(Sector.objects.all(), many=True).data,
            "nationality": NationalitySerializer(Nationality.objects.all(), many=True).data
        }

        return Response({"Success":True, "data":data}, status=HTTP_200_OK)

class UserDataView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(model=request.data.get('mobile'))
            return Response({"Success":True, "data":UserSerializer(user).data}, status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"Success":False, "Message":"Unknown User Mobile"}, status=HTTP_400_BAD_REQUEST)