from django.db import models
from django.conf import settings
from django.urls import reverse

class Table(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='cover/', blank=True)
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

class Review(models.Model):
    RATING_CHOICES = (
        ('1', 'Very Bad'),
        ('2', 'Bad'),
        ('3', 'Normal'),
        ('4', 'Good'),
        ('5', 'Perfect'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='review')
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    comment = models.TextField(blank=True) 
    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.table.name}"


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

    zarinpal_authority = models.CharField(max_length=255, blank=True, null=True)
    zarinpal_ref_id = models.CharField(max_length=150, blank=True, null=True)
    zarinpal_data = models.TextField(blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.reservation} - {self.status}"
    
    