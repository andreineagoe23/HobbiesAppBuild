from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import CustomUser, Hobby, FriendRequest
from .views import calculate_similarity  # Import your function

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        data = {'name': 'updated Name'}
        response = self.client.put('/api/profile/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated name')

class FriendRequestTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='user1', password='pass1')
        self.user2 = get_user_model().objects.create_user(username='user2', password='pass2')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_friend_request_send(self):
        response = self.client.post('/api/friend-requests/', {'to_user_id': self.user2.id})
        self.assertEqual(response.status_code, 201)

    def test_friend_request_accept(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.put('/api/friend-requests/', {'request_id': friend_request.id, 'action': 'accept'})
        self.assertEqual(response.status_code, 200)



#unit test to check the similarity works correctly
class SimilarityTestCase(TestCase):

    def setUp(self):
        # Create some test hobbies
        hobby1 = Hobby.objects.create(name="Reading")
        hobby2 = Hobby.objects.create(name="Gaming")
        hobby3 = Hobby.objects.create(name="Cooking")
        
        # Create some test users
        user1 = CustomUser.objects.create(username="user1", password="password1")
        user2 = CustomUser.objects.create(username="user2", password="password2")
        user3 = CustomUser.objects.create(username="user3", password="password3")
        
        # Assign hobbies to users
        user1.hobbies.add(hobby1, hobby2)
        user2.hobbies.add(hobby1, hobby3)
        user3.hobbies.add(hobby2, hobby3)
        
        # Save the users to the database
        user1.save()
        user2.save()
        user3.save()

    def test_calculate_similarity(self):
        user1 = CustomUser.objects.get(username="user1")
        user2 = CustomUser.objects.get(username="user2")
        user3 = CustomUser.objects.get(username="user3")
        
        all_users = CustomUser.objects.all()
        similarity_scores = calculate_similarity(user1, all_users)
        
        # Test expected similarity scores between users
        self.assertEqual(similarity_scores[user2.id], 1 / 3)  # user1 and user2 share 1 hobby out of 3 total hobbies
        self.assertEqual(similarity_scores[user3.id], 1 / 3)  # user1 and user3 share 1 hobby out of 3 total hobbies
        self.assertEqual(similarity_scores[user2.id], 1 / 3)  # user2 and user3 share 1 hobby out of 3 total hobbies
