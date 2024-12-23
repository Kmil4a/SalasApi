from django.db import models

from model_utils.models import SoftDeletableModel


class Room(SoftDeletableModel):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(SoftDeletableModel):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    description = models.CharField(max_length=240, default="No description")
    date = models.DateField()
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")
    confirmed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room.name} - {self.date} {self.start_time}"


class User(SoftDeletableModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name

