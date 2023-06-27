from django.urls import path
from .views import AllPetsViewSet, IndividualPetViewSet, VaccineViewSet, MedicationViewSet, AllergyViewSet

urlpatterns = [
    path('pets', AllPetsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pets/<int:id>', IndividualPetViewSet.as_view({'get': 'list', 'put': 'update'})),
    path('pets/<int:id>/vaccines', VaccineViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pets/<int:id>/medications', MedicationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pets/<int:id>/allergies', AllergyViewSet.as_view({'get': 'list', 'post': 'create'})),
]