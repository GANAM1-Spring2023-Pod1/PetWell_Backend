from django.urls import path
from .views import RegistrationView, SignInView, ProfileView

urlpatterns = [
    path('register', RegistrationView.as_view()),
    path('signin', SignInView.as_view()),
    path('profile', ProfileView.as_view())
]