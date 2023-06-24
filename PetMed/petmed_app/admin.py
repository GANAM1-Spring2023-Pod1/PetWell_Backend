from django.contrib import admin
from .models import UserProfile, Pet, Vaccine, Medication

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Pet)
admin.site.register(Vaccine)
admin.site.register(Medication)
