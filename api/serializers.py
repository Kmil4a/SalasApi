from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from api.models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'capacity',
            'is_active',
            'available'
        ]


class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id',
            'room',
            'description',
            'date',
            'start_time',
            'end_time',
            'confirmed',
            'canceled', 
        ]

class ReservationSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        return make_password(value)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()