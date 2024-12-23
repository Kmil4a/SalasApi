from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.utils.timezone import make_aware
from django.db.models import Q
from datetime import time, timedelta, datetime
from .serializers import RoomSerializer, RegisterSerializer, LoginSerializer, ReservationSerializer, ReservationSerializerPost
from .models import Reservation, Room


class Room_APIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print(request.user.is_superuser)
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({
            "user": {
                "is_superuser": request.user.is_superuser,
            },
            "rooms": serializer.data,
        })

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Room_APIView_Detail(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def get(self, request):
        reservations = Reservation.objects.all()

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        start_time = time.fromisoformat(data['start_time'])
        end_time = time.fromisoformat(data['end_time'])
        allowed_times = [time(h, 0) for h in range(9, 18)]

        if start_time not in allowed_times or end_time != (start_time.replace(hour=start_time.hour + 1)):
            return Response(
                {"error": "The reservation must be within 1-hour blocks from 9:00 to 18:00"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Reservation.objects.filter(
            room_id=data['room'],
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exists():
            return Response(
                {"error": "The selected time block is already reserved."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReservationSerializerPost(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Reservation_APIView_Detail(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def post(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.confirmed = True
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


class Reservation_APIView_Cancel(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        reservation = Reservation.objects.get(pk=pk)
        reservation.confirmed = False
        reservation.canceled = True
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeBlocksAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, room_id):

        start_hour = 9
        end_hour = 18
        time_blocks = []

        for hour in range(start_hour, end_hour):

            start_datetime = datetime.combine(datetime.today(), time(hour, 0))
            end_datetime = start_datetime + timedelta(hours=1)

            start_time = start_datetime.time()
            end_time = end_datetime.time()

            is_reserved = Reservation.objects.filter(
                room_id=room_id,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()

            time_blocks.append({
                'start_time': start_time.strftime('%H:%M'),
                'end_time': end_time.strftime('%H:%M'),
                'is_reserved': is_reserved,
            })

        return Response(time_blocks)
