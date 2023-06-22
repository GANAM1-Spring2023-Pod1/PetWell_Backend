from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from petmed_app.models import UserProfile
from petmed_app.serializers import UserProfileSerializer
from .serializers import UserSerializer

# Create your views here.
class RegistrationView(APIView):
    
    permission_classes = [permissions.AllowAny]

    # def get(self, request):
    #     result = User.objects.all()
    #     all_users = UserSerializer(
    #         result, 
    #         many = True
    #     )
    #     return Response(all_users.data)
    
    def post(self, request):
        user_data = self.request.data
        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]
        confirm_password = user_data["confirm_password"]
        try:
            if password == confirm_password:
                if User.objects.filter(username = username):
                    return Response({"Error": "Username already exists"})
                elif User.objects.filter(email = email):
                    return Response({"Error": "Email is associated with an existent account"})
                else:
                    new_user = User.objects.create_user(
                        username = username,
                        password = password
                    )
                    UserProfile.objects.create(
                        user = new_user, 
                        email = email, 
                        username = username
                    )
                    return Response({
                        "Success": "User Successfully Created",
                        "Token": AuthToken.objects.create(new_user)[1]
                    })
            else:
                return Response({"Error": "Passwords do not match"})
        except:
            return Response({"Error": "An issue occurred whilst attempting to register"})
        
class SignInView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        login_data = self.request.data
        username = login_data["username"]
        password = login_data["password"]
        try:
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return Response({
                    "Success": "User Successfully Authenticated",
                    "Token": AuthToken.objects.create(user)[1]
                })
            else:
                return Response({"Error": "User cannot be authenticated"})
        except:
            return Response({"Error": "An issue occurred whilst attempting to authenticate user"})

