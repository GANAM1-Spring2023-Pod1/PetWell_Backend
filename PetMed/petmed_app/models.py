from django.db import models
from django.contrib.auth.models import User
from .PET_TYPES import PET_TYPES

# User Profile Model (Based on Django User)
class UserProfile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )

    username = models.CharField(
        unique = True,
        max_length = 64
    )

    email = models.EmailField(
        unique = True,
        max_length = 64
    )

    def __str__(self):
        return self.username
    
class Pet(models.Model):

    owner = models.ForeignKey(
        UserProfile,
        on_delete = models.CASCADE
    )

    pet_name = models.CharField(
        max_length = 64
    )

    pet_type = models.CharField(
        max_length = 64,
        choices = PET_TYPES
    )

    def __str__(self):
        return self.pet_name
    
class Vaccine(models.Model):

    pet = models.ManyToManyField(
        Pet,
        on_delete = models.CASCADE
    )

    vaccine_name = models.CharField(
        max_length = 64,
        unique = True
    )

    vaccine_purpose = models.CharField(
        max_length = 128
    )

    vaccine_date_received = models.DateField()

    def __str__(self):
        return self.vaccine_name

class Medication(models.Model):

    pet = models.ManyToManyField(
        Pet,
        on_delete = models.CASCADE
    )

    medication_name = models.CharField(
        max_length = 64,
        unique = True
    )

    medication_purpose = models.CharField(
        max_length = 128
    )

    medication_date_taken = models.DateTimeField()

    def __str__(self):
        return self.medication_name