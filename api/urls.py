from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.urls import path

from .views import main_spa
from .views import signup_view, login_view, logout_view
from .views import UserProfileAPIView
from .views import FriendRequestAPIView

urlpatterns = [
    path('', main_spa),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/profile/', UserProfileAPIView.as_view(), name='profile'),
    path('api/friend-requests/', FriendRequestAPIView.as_view(), name='friend_requests'),
]
