from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken

from .serializers import UserProfileSerializer, PetSerializer, VaccineSerializer, MedicationSerializer, AllergySerializer
from .models import UserProfile, Pet, Vaccine, Medication, Allergy

# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class AllPetsViewSet(APIView):
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request):
        try:
            user = self.request.user
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                pet = request.data['pet']
                pet_type = request.data['pet_type']
                pet_dob = request.data['pet_dob']
                pet_gender = request.data['pet_gender']
                pet_weight = request.data['pet_weight']
                owner = UserProfile.objects.get(user = user)
                Pet.objects.create(owner = owner, pet_type = pet_type, pet_dob = pet_dob, pet_gender = pet_gender, pet_weight = pet_weight)
                return Response({"Success": "Pet Successfully Created"})
            else:
                return Response({"Error": "User not authenticated; please include an authentication token"})
        except Exception as e:
            print("Error", e)
            return Response({"Error": "Invalid request body"})
    
    def get(self, request):
        try: 
            results = Pet.objects.all()
            all_pets = PetSerializer(results, many = True)
            return Response(all_pets.data)
        except:
            return Response({"Error": "Something went wrong"})
        
class IndividualPetViewSet(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request, id):
        try:
            pet_results = Pet.objects.get(id = id)
            pet = PetSerializer(pet_results)
            vaccine_results = Vaccine.objects.filter(pet = id)
            vaccines = VaccineSerializer(vaccine_results)
            medication_results = Medication.objects.filter(pet = id)
            medications = MedicationSerializer(medication_results)
            allergy_results = Aller