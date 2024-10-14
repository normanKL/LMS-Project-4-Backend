from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import jwt
from .models import Profile

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)

        if user_to_create.is_valid():
            user_to_create.save()
            return Response({"message": "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail="Invalid Credentials")
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")
        
        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode({'sub': user_to_login.id, 'exp': int(dt.timestamp())}, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token, 'message': f"Welcome back {user_to_login.username}"})

class UserInfoView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        user = request.user
        user_profile, _ = Profile.objects.get_or_create(user=user)

        user_data = {
            '_id': user.id,
            'username': user.username,
            'email': user.email,
            'image_url': user.image_url,  
            'country': user.country,       
            'quote': user.quote,           
        }

        return Response(user_data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        # Ensure the profile exists
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        # Get or create the profile
        user_profile, created = Profile.objects.get_or_create(user=request.user)

        # Check if the request includes an image URL
        image_url = request.data.get('image_url')
        if image_url:
            user_profile.image_url = image_url  # Set the image URL
            user_profile.save()
        
        # Update the profile with incoming data
        serializer = ProfileSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
