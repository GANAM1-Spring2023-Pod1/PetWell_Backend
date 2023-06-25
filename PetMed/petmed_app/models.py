from django.db import models
from django.contrib.auth.models import User
from .PET_TYPES import PET_TYPES, GENDERS

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

    user_firstname = models.CharField(
        max_length = 64
    )

    user_lastname = models.CharField(
        max_length = 64
    )

    def __str__(self):
        return self.user_firstname
    
class Pet(models.Model):

    owner = models.ForeignKey(
        UserProfile,
        on_delete = models.CASCADE
    )

    pet = models.CharField(
        max_length = 64
    )

    pet_type = models.CharField(
        max_length = 64,
        choices = PET_TYPES
    )

    pet_breed = models.CharField(
        max_length = 128
    )

    pet_dob = models.DateField()

    pet_gender = models.CharField(
        choices = GENDERS
    )

    pet_weight = models.IntegerField()

    def __str__(self):
        return self.pet
    
class Vaccine(models.Model):

    pet = models.ForeignKey(
        Pet,
        on_delete = models.CASCADE
    )

    vaccine = models.CharField(
        max_length = 128,
        unique = True
    )

    vaccine_date = models.DateField()

    vaccine_end = models.DateField()

    def __str__(self):
        return self.vaccine_name

class Medication(models.Model):

    pet = models.ForeignKey(
        Pet,
        on_delete = models.CASCADE
    )

    medication = models.CharField(
        max_length = 128,
    )

    medication_frequency = models.CharField(
        max_length = 64
    )

    medication_date = models.DateTimeField()

    def __str__(self):
        return self.medication
    
class Allergy(models.Model):

    pet = models.ForeignKey(
        Pet,
        on_delete = models.CASCADE
    )

    allergy = models.CharField()

    allergy_desc = models.TextField()

    def __str__(self):
        return self.allergy