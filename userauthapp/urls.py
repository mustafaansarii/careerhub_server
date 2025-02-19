from django.urls import path
from . import views

urlpatterns = [
    path('send-otp/', views.send_otp, name='send_otp'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
] 