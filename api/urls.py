from django.urls import path
from .views import (
    main_spa, signup_view, login_view, logout_view,
    UserProfileAPIView, api_login, api_signup, get_hobbies, send_friend_request, accept_friend_request, fetch_friend_requests, list_users
)

urlpatterns = [
    path('', main_spa, name='main_spa'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/login/', api_login, name='api_login'),
    path('api/profile/', UserProfileAPIView.as_view(), name='profile'),
    path('api/signup/', api_signup, name='api_signup'),
    path('api/hobbies/', get_hobbies, name='get_hobbies'),
    path('api/users/', list_users, name='list_users'),
    path('api/friend-requests/send/', send_friend_request, name='send_friend_request'),
    path('api/friend-requests/accept/', accept_friend_request, name='accept_friend_request'),
    path('api/friend-requests/', fetch_friend_requests, name='fetch_friend_requests'),
]

