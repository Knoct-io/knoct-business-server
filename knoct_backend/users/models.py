from django.utils import timezone
from django.db import models


class Enterprise(models.Model):
    registration_number = models.BigIntegerField(null=False, blank=False, db_index=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, db_index=True)
    sector = models.ForeignKey(to='Sector', related_name='enterprise_sector', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_employees = models.IntegerField(default=1)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'enterprises'


class Sector(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sector'


class User(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False, default=None, db_index=True)
    mobile = models.BigIntegerField(unique=True, blank=False, null=False, db_index=True)
    city = models.ForeignKey(to='City', related_name='user_city',blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_logged_in_time = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateTimeField()
    privilege = models.ForeignKey(to='Privilege', related_name='user_privilege', on_delete=models.CASCADE, default='User')
    enterprise = models.ForeignKey(to='Enterprise', related_name='user_enterprise', on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(default=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    documents_uploaded_count = models.IntegerField(default=0)
    documents_verified_count = models.IntegerField(default=0)
    public_key = models.CharField(max_length=100, unique=True, null=True)
    class Meta:
        db_table = 'users'


class City(models.Model):
    name = models.CharField(max_length=50, default=None)
    state = models.ForeignKey(to='State', related_name='city_state', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cities'


class State(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'state'


class Privilege(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'privileges'


class MobileOtpLogs(models.Model):
    mobile = models.BigIntegerField()
    otp = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mobile_otps'


class EmailOtpLogs(models.Model):
    email = models.EmailField()
    otp = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_otps'

class Nationality(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'nationality'