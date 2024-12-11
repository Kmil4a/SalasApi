from rest_framework import serializers
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