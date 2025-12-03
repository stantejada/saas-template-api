from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
]



