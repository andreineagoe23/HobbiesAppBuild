from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Hobby, FriendRequest
from .serializers import UserProfileSerializer, FriendRequestSerializer


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): # serializes user profile data and returns it as one.
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request): # edit user details 
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists(): # returns if user request already exists.
                return Response({'error': 'You have already sent a friend reqeust to this user!'}, status=400) 

            FriendRequest.objects.create(from_user=request.user, to_user=to_user) # if the user exists and no request has already been sent, send the rqeeuest. then return.
            return Response({'message': 'Friend request successfully sent!'}, status=201)

        except CustomUser.DoesNotExist: # if user doesn't exist, return.
            return Response({'error': 'User doesnt exist.'}, status=404)

    def get(self, request):
        # gets a list of all the user's outstanding friend reqeuests.
        received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = FriendRequestSerializer(received_requests, many=True)
        return Response(serializer.data)

    def put(self, request):
        # when the user accepts a friend request
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)

            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                return Response({'message': 'You have accepted the friend request!'})
            elif action == 'reject':
                friend_request.delete()
                return Response({'message': 'You have rejected the friend request!'})
            else:
                return Response({'error': 'action not supported...'}, status=400)

        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request does not exist.'}, status=404)


# left in the template. not sure what this does.
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

# sign up 
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # this can be changed. to whatever should the front page after you sign up.
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# login .
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# logout.
def logout_view(request):
    logout(request)
    return redirect('login')  # go to login page after you log out.

    
