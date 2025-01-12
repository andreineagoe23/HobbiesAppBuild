from django.urls import path
from .views import (
    main_spa, signup_view, login_view, logout_view,
    UserProfileAPIView, api_login, api_signup, get_hobbies, get_similar_users
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
    path('api/similar-users/', get_similar_users, name='get_similar_users'),
]

