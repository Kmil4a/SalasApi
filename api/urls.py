from django.urls import path
from .views import RegisterAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (Room_APIView, Room_APIView_Detail, Reservation_APIView,
                    Reservation_APIView_Detail, Reservation_APIView_Confirm,
                    Reservation_APIView_Cancel, TimeBlocksAPIView)

urlpatterns = [
    path('room', Room_APIView.as_view(), name='room'),
    path('room/<int:pk>', Room_APIView_Detail.as_view(), name='room_detail'),
    path('reservas', Reservation_APIView.as_view(), name='reservas'),
    path('reservas/<int:pk>', Reservation_APIView_Detail.as_view(),
         name='reservas_detail'),
    path('reservas/<int:pk>/checkin',
         Reservation_APIView_Confirm.as_view(), name='reservas_checkin'),
    path('reservas/<int:pk>/cancel',
         Reservation_APIView_Cancel.as_view(), name='reservas_cancel'),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rooms/<int:room_id>/time-blocks/', TimeBlocksAPIView.as_view(), name='time_blocks'),
]
