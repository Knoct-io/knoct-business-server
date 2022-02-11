from rest_framework import serializers

from .models import Sector, Privilege, City, State, User

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['id', 'name', 'created_at']


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()
    class Meta:
        model = City
        fields = ['id', 'name', 'created_at', 'state']


class PrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        fields = ['id', 'name', 'created_at']


class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = ['id', 'name', 'created_at']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'city', 'created_at', 'updated_at', 'last_logged_in_time', 'date_of_birth',\
            'privilege', 'enterprise', 'is_active', 'mobile_verified', 'email_verified', 'documents_uploaded_count', \
            'documents_verified_count', 'public_key']
