from django.contrib import admin
from .models import CustomUser, Hobby, FriendRequest

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'name', 'date_of_birth']

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status', 'created_at']
