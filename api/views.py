from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer
from .models import Reservation
from .serializers import ReservationSerializer
from .serializers import ReservationSerializerPost


class Room_APIView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Room_APIView_Detail(APIView):
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = Room.objects.get(pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = Room.objects.get(pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Reservation_APIView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializerPost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Reservation_APIView_Detail(APIView):
    def get(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Reservation_APIView_Confirm(APIView):
    def post(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.confirmed = True
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


class Reservation_APIView_Cancel(APIView):
    def post(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.confirmed = False
        reservation.canceled = True
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
