from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.cache import cache
from datetime import datetime, timedelta

# Create your views here.

def generate_otp():
    return str(random.randint(100000, 999999))

@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate OTP and store in cache with 5 minutes expiry
    otp = generate_otp()
    otp_data = {
        'otp': otp,
        'timestamp': datetime.now().timestamp()
    }
    
    # Store OTP data in cache
    cache.set(f'otp_{email}', otp_data, timeout=300)  # 5 minutes
    
    # Send OTP via email
    try:
        send_mail(
            'Your OTP for Registration',
            f'Your OTP for registration is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    if not email or not otp:
        return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get stored OTP data from cache
    stored_otp_data = cache.get(f'otp_{email}')
    
    if not stored_otp_data:
        return Response({'error': 'No OTP found. Please request a new OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check OTP expiration
    otp_timestamp = stored_otp_data['timestamp']
    current_time = datetime.now().timestamp()
    
    if current_time - otp_timestamp > 300:  # 5 minutes in seconds
        # Clear expired OTP
        cache.delete(f'otp_{email}')
        return Response({'error': 'OTP has expired. Please request a new OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify OTP
    if otp != stored_otp_data['otp']:
        return Response({'error': 'Incorrect OTP. Please try again'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_verified = True
        user.save()
        
        # Clear cache after successful registration
        cache.delete(f'otp_{email}')
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(email=email, password=password)
    if user:
        if user.is_verified:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Please verify your email'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = None
        user.save()
        return Response({'message': 'Email verified successfully'})
    except User.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
