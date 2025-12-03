from django.contrib import admin
from .models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
