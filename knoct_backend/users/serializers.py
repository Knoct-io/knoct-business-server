from rest_framework import serializers

from .models import Sector, Privilege, City, State

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