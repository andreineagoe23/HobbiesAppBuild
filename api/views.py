from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Hobby, FriendRequest
from .serializers import UserProfileSerializer, FriendRequestSerializer
from django.contrib.auth import get_user_model
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.db import IntegrityError
from django import forms

CustomUser = get_user_model()

def main_spa(request):
    return render(request, 'index.html')

@api_view(['POST'])
def api_signup(request):
    data = request.data
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Validate required fields
    if not email or not username or not password:
        return Response({'error': 'All fields are required.'}, status=HTTP_400_BAD_REQUEST)

    try:
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=HTTP_400_BAD_REQUEST)

        # Create the user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User created successfully.'}, status=HTTP_201_CREATED)
    
    except IntegrityError as e:
        return Response({'error': 'Database error. Please try again.'}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log unexpected errors
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
