from rest_framework import serializers
from .models import CustomUser, Hobby, FriendRequest

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    hobbies = HobbySerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'email', 'date_of_birth', 'hobbies']

    def update(self, instance, validated_data):
        hobbies_data = validated_data.pop('hobbies', [])
        instance = super().update(instance, validated_data)

        # Update or create hobbies if necessary
        if hobbies_data:
            instance.hobbies.clear()
            for hobby_data in hobbies_data:
                hobby, created = Hobby.objects.get_or_create(**hobby_data)
                instance.hobbies.add(hobby)

        return instance

# serializer for friend requests.
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
