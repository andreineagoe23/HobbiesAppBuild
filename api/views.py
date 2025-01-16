from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django import forms
from rest_framework.authtoken.models import Token
from .models import CustomUser, Hobby, FriendRequest, Friendship
from .serializers import UserProfileSerializer, FriendRequestSerializer, HobbySerializer
from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response


CustomUser = get_user_model()

def main_spa(request):
    return render(request, 'index.html')

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
def api_signup(request):
    data = request.data
    email = data.get('email')
    username = email
    password = data.get('password')
    name = data.get('name')
    date_of_birth = data.get('date_of_birth')
    hobbies = data.get('hobbies', [])  # List of hobby IDs

    # Validate required fields
    if not email or not username or not password or not name or not date_of_birth:
        print("all fields required")
        return Response({'error': 'All fields are required.'}, status=HTTP_400_BAD_REQUEST)

    try:
        if CustomUser.objects.filter(email=email).exists():
            print("email already exists")
            return Response({'error': 'Email already exists.'}, status=HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            print("username already exists.")
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
        print("Signup success!")
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
        print(f"Processing accept request for ID: {request_id}")

        # Fetch the friend request
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user, status='pending')
        print(f"Found friend request: {friend_request}")

        # Update the status to accepted
        friend_request.status = 'accepted'
        friend_request.save()
        print("Friend request status updated to 'accepted'")

        # Create a friendship (ensure user1 < user2 for consistency)
        user1, user2 = sorted([friend_request.from_user, request.user], key=lambda x: x.id)
        friendship, created = Friendship.objects.get_or_create(user1=user1, user2=user2)
        if created:
            print(f"Friendship created between {user1} and {user2}")
        else:
            print(f"Friendship already exists between {user1} and {user2}")

        return Response({'message': 'Friend request accepted'}, status=HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        print(f"Friend request not found or already processed for ID: {request_id}")
        return Response({'error': 'Friend request not found or already processed'}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error accepting friend request: {str(e)}")
        return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_friend_requests(request):
    try:
        print(f"Fetching friend requests for User ID: {request.user.id}")  # Log user ID
        requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        print(f"Pending Friend Requests Count: {requests.count()}")  # Log request count
        print(f"Pending Friend Requests: {requests.values('id', 'from_user__name')}")  # Log request details

        serializer = FriendRequestSerializer(requests, many=True)
        return Response({'requests': serializer.data}, status=HTTP_200_OK)
    except Exception as e:
        print(f"Error in fetch_friend_requests: {str(e)}")  # Log errors
        return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eligible_for_friend_requests(request):
    try:
        exclude_user_id = request.user.id
        print(f"Authenticated User ID: {exclude_user_id}")  # Log authenticated user ID

        # Get all users except the logged-in user
        users = CustomUser.objects.exclude(id=exclude_user_id)
        print(f"Initial User Count (excluding self): {users.count()}")  # Log user count

        # Exclude users with existing friend requests
        users_with_requests = FriendRequest.objects.filter(
            from_user=request.user
        ).values_list('to_user', flat=True)
        print(f"Users with Existing Friend Requests: {list(users_with_requests)}")  # Log excluded users

        users = users.exclude(id__in=users_with_requests)
        print(f"Eligible User Count (after exclusions): {users.count()}")  # Log eligible user count
        print(f"Eligible Users: {users.values('id', 'name')}")  # Log eligible user details

        # Paginate the results
        paginator = Paginator(users, 10)  # 10 users per page
        page_number = request.query_params.get('page', 1)
        paginated_users = paginator.get_page(page_number)

        serializer = UserProfileSerializer(paginated_users, many=True)
        return Response({
            'results': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': paginated_users.number
        }, status=HTTP_200_OK)
    except Exception as e:
        print(f"Error in eligible_for_friend_requests: {str(e)}")  # Log errors
        return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    try:
        exclude_user_id = request.user.id
        min_age = request.query_params.get('min_age')
        max_age = request.query_params.get('max_age')

        # Fetch all users except the current user
        users = CustomUser.objects.exclude(id=exclude_user_id)

        # Filter users by age if parameters are provided
        if min_age:
            users = users.filter(date_of_birth__lte=f"{2025 - int(min_age)}-01-01")
        if max_age:
            users = users.filter(date_of_birth__gte=f"{2025 - int(max_age)}-01-01")


        # Get the hobbies of the currently authenticated user as a set
        #set intersection to be used to find similarity score in this case
        #if this works, then cool otherwise i am adding simpler get method dow commmented
        current_user_hobbies = set(request.user.hobbies.values_list('id', flat=True))

        # Calculate the similarity score for each user based on common hobbies
        user_similarity_scores = []

        # Iterate over all users in the database
        for user in users:
            # Get the hobbies for each user
            user_hobbies = set(user.hobbies.values_list('id', flat=True))

            # Calculate the intersection of hobbies (common hobbies)
            common_hobbies = current_user_hobbies.intersection(user_hobbies)
            similarity_score = len(common_hobbies) # Similarity score is the count of common hobbies

            # Append the user with their similarity score as a tuple
            user_similarity_scores.append((user, similarity_score))

        # Sort users by similarity score in descending order
        sorted_users = sorted(user_similarity_scores, key=lambda x: x[1], reverse=True)

        # Log for debugging
        print(f"Filtered Users: {users.values('id', 'name', 'date_of_birth')}")
        print(f"Filters: min_age={min_age}, max_age={max_age}")
        
        # Paginate results
        paginator = Paginator(users, 10)  # 10 users per page
        page_number = request.query_params.get('page', 1)
        paginated_users = paginator.get_page(page_number)

        serializer = UserProfileSerializer(paginated_users, many=True)
        return Response({
            'results': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': paginated_users.number
        }, status=HTTP_200_OK)
    except Exception as e:
        print(f"Error in list_users: {str(e)}")
        return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_friends(request):
    #gets all the users friends.
    try:
        user = request.user

        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))


        friends = []
        for friendship in friendships:
            if friendship.user1 == user:
                friends.append(friendship.user2)
            else:
                friends.append(friendship.user1)

        # Serialize 
        serializer = UserProfileSerializer(friends, many=True)
        return Response({"friends": serializer.data}, status=HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------this is the simpler get method for list_users-------------------

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_users(request):
#     try:
#         exclude_user_id = request.user.id
#         min_age = request.query_params.get('min_age')
#         max_age = request.query_params.get('max_age')

#         # Fetch all users except the current user
#         users = CustomUser.objects.exclude(id=exclude_user_id)

#         # Filter users by age if parameters are provided
#         if min_age:
#             users = users.filter(date_of_birth__lte=f"{2025 - int(min_age)}-01-01")
#         if max_age:
#             users = users.filter(date_of_birth__gte=f"{2025 - int(max_age)}-01-01")

#         # Get the hobbies of the currently authenticated user
#         current_user_hobbies = set(request.user.hobbies.values_list('id', flat=True))

#         # Initialize a list to store users and their similarity score
#         user_similarity_scores = []

#         # Loop over users and calculate the similarity score for each one
#         for user in users:
#             # Get the user's hobbies
#             user_hobbies = set(user.hobbies.values_list('id', flat=True))

#             # Initialize similarity score
#             similarity_score = 0

#             # Manually count the matching hobbies
#             for hobby in user_hobbies:
#                 if hobby in current_user_hobbies:
#                     similarity_score += 1

#             # Append the user with their similarity score
#             user_similarity_scores.append((user, similarity_score))

#         # Sort the users based on the similarity score (descending order)
#         sorted_users = sorted(user_similarity_scores, key=lambda x: x[1], reverse=True)

#         # Paginate the sorted users list
#         paginator = Paginator(sorted_users, 10)
#         page_number = request.query_params.get('page', 1)
#         paginated_users = paginator.get_page(page_number)

#         # Serialize the users and return the response
#         serializer = UserProfileSerializer(paginated_users, many=True)
#         return Response({
#             'results': serializer.data,
#             'total_pages': paginator.num_pages,
#             'current_page': paginated_users.number
#         }, status=HTTP_200_OK)

#     except Exception as e:
#         print(f"Error in list_users: {str(e)}")
#         return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)