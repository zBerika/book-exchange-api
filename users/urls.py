# users/urls.py
from django.urls import path
from .views import UserRegistrationView, UserLoginView, LogoutView, UserProfileView # Исправленные импорты

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]