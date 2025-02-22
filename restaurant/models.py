from django.db import models
from django.conf import settings
from django.urls import reverse

class Table(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"
    
    def get_absolute_url(self):
        return reverse('reserve_table', args=[self.id])
    
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_pepole = models.IntegerField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.date} at {self.time}"
