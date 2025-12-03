from django.urls import path, include
from rest_framework.routers import DefaultRouter #type:ignore
from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



