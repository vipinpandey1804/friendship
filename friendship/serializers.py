from rest_framework import serializers
from friendship.models import FriendshipRequest, Friend, Follow, Block
from base_user.models import User

class AddFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ['to_user', 'message']
    # to_user = serializers.UUIDField(required=True)
    # message = serializers.CharField(required=False)

class FriendshipRequestIdSerializer(serializers.Serializer):
    friend_request_id = serializers.IntegerField()

class FriendRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

class UserIdSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)

class FollowListSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = User
        fields = '__all__'

class BlockListSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = User
        fields = '__all__'

class FriendDetailsUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    class Meta:
        model = User
        fields = ['id','full_name','email','phone', 'avatar']

class DeleteFromUserFriendDetailsSerializer(serializers.ModelSerializer):
    to_user = FriendDetailsUserSerializer()
    class Meta:
        model = Friend
        fields = ['id', 'created', 'to_user']

class DeleteToUserFriendDetailsSerializer(serializers.ModelSerializer):
    from_user = FriendDetailsUserSerializer()
    class Meta:
        model = Friend
        fields = ['id', 'created', 'from_user']