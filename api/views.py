from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django import forms
from rest_framework.authtoken.models import Token
from .models import CustomUser, Hobby, FriendRequest
from .serializers import UserProfileSerializer, FriendRequestSerializer, HobbySerializer
from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import CustomUser
from django.db.models import Q

CustomUser = get_user_model()

#filtering by age (users list)
def filter_users_with_pagination(request):
    if request.method == 'GET':
        try:
            # Get query parameters
            min_age = request.GET.get('min_age', None)
            max_age = request.GET.get('max_age', None)
            page_number = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)  # Default page size

            today = datetime.today()
            min_dob = today - timedelta(days=int(max_age) * 365) if max_age else None
            max_dob = today - timedelta(days=int(min_age) * 365) if min_age else None

            # Filter users by age
            users = CustomUser.objects.all()
            if min_dob:
                users = users.filter(date_of_birth__lte=min_dob)
            if max_dob:
                users = users.filter(date_of_birth__gte=max_dob)

            # Paginate the results
            paginator = Paginator(users, page_size)
            page = paginator.get_page(page_number)

            # Serialize the paginated data
            user_data = [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "date_of_birth": user.date_of_birth,
                    "hobbies": [hobby.name for hobby in user.hobbies.all()],
                }
                for user in page
            ]

            return JsonResponse({
                "users": user_data,
                "total_pages": paginator.num_pages,
                "current_page": page.number,
                "total_users": paginator.count
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)

def main_spa(request):
    return render(request, 'index.html')

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
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

        # Log in the user and generate a token
        from django.contrib.auth import authenticate
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'error': 'Authentication failed.'}, status=HTTP_400_BAD_REQUEST)

        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'User created successfully.',
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'dob': user.date_of_birth,
                'hobbies': list(user.hobbies.values('id', 'name'))
            }
        }, status=HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)


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
            print(f"Token for user {user.email}: {token.key}")  # Debugging log
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
        """
        Retrieve the authenticated user's profile.
        """
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """
        Update the authenticated user's profile.
        """
        print("Authenticated user:", request.user)  # Debugging log
        print("Received data:", request.data)      # Debugging log

        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("Saved data:", serializer.data)  # Debugging log
            return Response(serializer.data)
        else:
            print("Validation errors:", serializer.errors)  # Debugging log
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
@permission_classes([AllowAny])
def get_hobbies(request):
    try:
        hobbies = Hobby.objects.all()
        serializer = HobbySerializer(hobbies, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": f"Unable to fetch hobbies: {str(e)}"}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get('to_user_id')
    if not to_user_id:
        return Response({'error': 'Recipient user ID is required.'}, status=HTTP_400_BAD_REQUEST)
    try:
        to_user = CustomUser.objects.get(id=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists():
            return Response({'error': 'Friend request already sent.'}, status=HTTP_400_BAD_REQUEST)
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({'message': 'Friend request sent successfully.'}, status=HTTP_201_CREATED)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    request_id = request.data.get('request_id')
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        if friend_request.status == 'accepted':
            return Response({'error': 'Request already accepted.'}, status=HTTP_400_BAD_REQUEST)
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({'message': 'Friend request accepted.'}, status=HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_friend_requests(request):
    try:
        page = request.query_params.get('page', 1)
        per_page = 10
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending').select_related('from_user')
        paginator = Paginator(pending_requests, per_page)
        paginated_requests = paginator.get_page(page)
        serializer = FriendRequestSerializer(paginated_requests, many=True)
        return Response({
            'requests': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': paginated_requests.number
        }, status=HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    exclude_user_id = request.user.id
    users = CustomUser.objects.exclude(id=exclude_user_id)
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)
