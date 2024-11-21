from django.db import models

from model_utils.models import SoftDeletableModel

class Room(SoftDeletableModel):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Reservation(SoftDeletableModel):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room.name} - {self.date} {self.time}"

