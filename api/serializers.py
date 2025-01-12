from rest_framework import serializers
from .models import CustomUser, Hobby, FriendRequest

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    # Accepts IDs for hobbies during updates but returns full details for GET
    hobbies = serializers.PrimaryKeyRelatedField(many=True, queryset=Hobby.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'date_of_birth', 'hobbies']

    def to_representation(self, instance):
        """
        Convert the user instance into a format that includes detailed hobby info.
        """
        representation = super().to_representation(instance)
        representation['hobbies'] = HobbySerializer(instance.hobbies.all(), many=True).data
        return representation

# serializer for friend requests.
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
