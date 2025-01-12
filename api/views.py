from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Hobby, FriendRequest
from .serializers import UserProfileSerializer, FriendRequestSerializer, HobbySerializer
from django.contrib.auth import get_user_model
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.db import IntegrityError
from django import forms
from collections import Counter


CustomUser = get_user_model()

def main_spa(request):
    return render(request, 'index.html')

@api_view(['POST'])
def api_signup(request):
    data = request.data
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    date_of_birth = data.get('date_of_birth')
    hobbies = data.get('hobbies', [])  # List of hobby IDs

    # Validate required fields
    if not email or not username or not password or not name or not date_of_birth:
        return Response({'error': 'All fields are required.'}, status=HTTP_400_BAD_REQUEST)

    try:
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            date_of_birth=date_of_birth,
        )

        for hobby_id in hobbies:
            try:
                hobby = Hobby.objects.get(id=hobby_id)
                user.hobbies.add(hobby)
            except Hobby.DoesNotExist:
                continue

        user.save()
        return Response({'message': 'User created successfully.'}, status=HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def api_login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=400)

        # Authenticate using email as the username field
        user = authenticate(request, username=email, password=password)
        if user:
            # Include all required fields in the response
            return Response({
                'token': 'dummy_token',  # Replace with an actual token if using token-based auth
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'dob': user.date_of_birth,
                    'hobbies': list(user.hobbies.values('id', 'name'))
                }
            }, status=200)

        return Response({'error': 'Invalid credentials'}, status=401)

    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response({'error': 'Internal server error'}, status=500)

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Update hobbies if provided
            if 'hobbies' in request.data:
                hobbies_data = request.data['hobbies']
                user.hobbies.set(hobbies_data)
                user.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Hobbies"
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'username', 'date_of_birth', 'hobbies', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'api/spa/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
def get_hobbies(request):
    try:
        hobbies = Hobby.objects.all()
        serializer = HobbySerializer(hobbies, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching hobbies: {str(e)}")
        return Response({"error": "Unable to fetch hobbies. Please try again later."}, status=500)


def calculate_similarity(user, all_users):
    """
    Calculate the similarity of hobbies between a user and all other users.
    Returns a list of tuples (other_user, similarity_score) sorted by similarity_score in descending order.
    """
    # Get the set of hobbies for the current user
    user_hobbies = set(user.hobbies.values_list('id', flat=True))

    # Prefetch hobbies for all users to avoid redundant database queries
    all_users = all_users.prefetch_related('hobbies')

    similarity = []  # List to store similarity tuples (other_user, similarity_score)

    for other_user in all_users:
        if other_user != user:  # Skip the user itself
            # Get the set of hobbies for the other user
            other_user_hobbies = set(other_user.hobbies.values_list('id', flat=True))

            # Calculate common and union of hobbies
            common_hobbies = user_hobbies.intersection(other_user_hobbies)
            total_hobbies = user_hobbies.union(other_user_hobbies)

            # Avoid division by zero, only consider users with at least one hobby
            if len(total_hobbies) > 0:
                similarity_score = len(common_hobbies) / len(total_hobbies)
                similarity.append((other_user, similarity_score))

    # Sort by similarity score in descending order
    similarity.sort(key=lambda x: x[1], reverse=True)

    return similarity
    

#similar users view
@api_view(['GET'])
def get_similar_users(request):
    try:
        # Get the current authenticated user
        user = request.user
        
        # Fetch all users from the database
        all_users = CustomUser.objects.all()

        # Calculate similarity using your function
        similarity_scores = calculate_similarity(user, all_users)  # or calculate_hobby_similarity
        
        # Limit the number of users returned (for example, top 10)
        top_similar_users = similarity_scores[:10]
        
        # Format the response
        response_data = [{
            'user_id': other_user.id,
            'username': other_user.username,
            'similarity_score': similarity_score
        } for other_user, similarity_score in top_similar_users]

        return Response({'similar_users': response_data}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
