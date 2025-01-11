from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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
