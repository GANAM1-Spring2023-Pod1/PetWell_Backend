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

class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer

class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer

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
                pet_breed = request.data['pet_breed']
                pet_dob = request.data['pet_dob']
                pet_gender = request.data['pet_gender']
                pet_weight = request.data['pet_weight']
                owner = UserProfile.objects.get(user = user)
                Pet.objects.create(owner = owner, pet = pet, pet_type = pet_type, pet_breed = pet_breed, pet_dob = pet_dob, pet_gender = pet_gender, pet_weight = pet_weight)
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
            allergy_results = Allergy.objects.filter(pet = id)
            allergies = AllergySerializer(allergy_results)
            return Response({"Pet": pet.data, "Vaccines": vaccines.data, "Medications": medications.data, "Allergies": allergies.data})
        except Exception as e:
            print("Error Retrieving Single Pet:", e)
            return Response({"Error": "Something went wrong"})
        
    def put(self, request, id):
        try:
            user = self.request.user
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                pet_type = request.data['pet_type']
                pet_dob = request.data['pet_dob']
                pet_gender = request.data['pet_gender']
                pet_weight = request.data['pet_weight']
                pet = request.data['pet']
                # owner = UserProfile.objects.get(user = user)
                pet_instance = Pet.objects.get(id = id)
                # if owner.id == pet_instance.owner:
                    # pet.pet_type = pet_type
                    # pet.pet_dob = pet_dob
                    # pet.pet_gender = pet_gender
                    # pet.pet_weight = pet_weight
                    # pet.pet = pet_name
                    # pet.save()
                pet_instance.objects.update(pet_type = pet_type, pet_dob = pet_dob, pet_gender = pet_gender, pet_weight = pet_weight, pet = pet)
                res = f'Pet {pet_instance.id} has been successfully updated'
                return Response({"Success": res})
                # else:
                #     return Response({"Error": f"User {owner.id} not authorized to update pet {pet.owner}"})
            else:
                return Response({"Error": "User not authenticated; please include an authorization token"})
        except Exception as e:
            print("Error", e)
            return Response({"Error": "Invalid request body"})
        
    def delete(self, request, id):
        try:
            user = self.request.user
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                userProfile = UserProfile.objects.get(user = user)
                petProfile = Pet.objects.get(id = id)
                if str(userProfile.id) == str(petProfile.owner):
                    petProfile.delete()
                    return Response({"Success": "Pet successfully deleted"})
                else:
                    return Response({"Error": "User not authorized to delete pet"})
            else:
                return Response({"Error": "User not authenticated; please provide an authorization token"})
        except:
            return Response({"Error": "Invalid Request Body"})

        
class IndividualVaccineViewSet(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, id):
        try:
            user = self.request.user
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                vaccine = request.data['vaccine']
                vaccine_date = request.data['vaccine_date']
                vaccine_end = request.data['vaccine_end']
                pet = Pet.objects.get(id = id)
                Vaccine.objects.create(vaccine = vaccine, vaccine_date = vaccine_date, vaccine_end = vaccine_end, pet = pet)
                return Response({"Success": "Vaccine record successfully created"})
            else:
                return Response({"Error": "User not authenticated; please include an authentication token"})
        except:
            return Response({"Error": "Error likely caused by invalid request body"})


class IndividualMedicationViewSet(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, id):
        try:
            user = self.request.user
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                medication = request.data['medication']
                medication_date = request.data['medication_date']
                medication_frequency = request.data['medication_frequency']
                pet = Pet.objects.get(id = id)
                Medication.objects.create(medication = medication, medication_date = medication_date, medication_frequency = medication_frequency, pet = pet)
                return Response({"Success": "Medication record successfully created"})
            else:
                return Response({"Error": "User not authenticated; please include an authentication token"})
        except:
            return Response({"Error": "Error likely caused by invalid request body"})


class IndividualAllergyViewSet(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, id):
        try:
            user = self.request.user
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                allergy = request.data['allergy']
                pet = Pet.objects.get(id = id)
                Allergy.objects.create(allergy = allergy, pet = pet)
                return Response({"Success": "Allergy record successfully created"})
            else:
                return Response({"Error": "User not authenticated; please include an authentication token"})
        except:
            return Response({"Error": "Error likely caused by invalid request body"})