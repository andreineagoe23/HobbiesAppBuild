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
from rest_framework.authtoken.models import Token


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


from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
def api_login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=400)

        user = authenticate(request, username=email, password=password)
        if user:
            # Generate or retrieve the token
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
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


