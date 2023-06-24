from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken

from .serializers import UserProfileSerializer, PetSerializer, VaccineSerializer, MedicationSerializer
from .models import UserProfile, Pet, Vaccine, Medication

# Create your views here.

# User Registration View Set
