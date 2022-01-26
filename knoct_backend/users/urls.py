from django.urls import path
from . import views


urlpatterns = [
     path('addenterprise/',views.AddEnterpriseView.as_view()),
     path('usersignup/',views.UserSignUpView.as_view()),
     path('userlogin/',views.UserLoginView.as_view()),
     path('verify_otp/',views.VerifyOtpView.as_view()),
]