from django.urls import path
from . import views


urlpatterns = [
     path('add_enterprise/',views.AddEnterpriseView.as_view()),
     path('user_signup/',views.UserSignUpView.as_view()),
     path('user_login/',views.UserLoginView.as_view()),
     path('verify_otp/',views.VerifyOtpView.as_view()),
     path('verify_otp/',views.VerifyOtpView.as_view()),
     path('site_configurations/',views.SiteConfigView.as_view()),
]