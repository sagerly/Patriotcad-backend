from django.contrib.auth.models import User  # Import Django's built-in User model
from django.db import models
from django.utils import timezone

# New model for Officers
class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    badge_number = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.badge_number} - {self.department}"

# New model for Civilian

class Civilian(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    
    def __str__(self):  # Add this method
        return f"{self.first_name} {self.last_name}"

class Citation(models.Model):
    description = models.CharField(max_length=255)
    date_issued = models.DateField()
    civilians = models.ManyToManyField(Civilian, related_name='citations')

class Arrest(models.Model):
    description = models.CharField(max_length=255)
    date_arrested = models.DateField()
    civilians = models.ManyToManyField(Civilian, related_name='arrests')

class Warrant(models.Model):
    description = models.CharField(max_length=255)
    date_issued = models.DateField()
    civilians = models.ManyToManyField(Civilian, related_name='warrants')

class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=10)
    civilians = models.ManyToManyField(Civilian, related_name='vehicles')


# New model for Current Calls
class CurrentCall(models.Model):
    description = models.CharField(max_length=255)
    time_of_call = models.DateTimeField(default=timezone.now)
    assigned_officers = models.ManyToManyField(User, related_name='assigned_calls')  # Use User here
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)

    def __str__(self):
        return f"{self.description} - Priority {self.priority}"