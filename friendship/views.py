from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from friendship.models import Friend, FriendshipRequest, Follow, Block
from base_user.models import User
from friendship.serializers import AddFriendSerializer, FriendshipRequestIdSerializer, FriendRequestListSerializer, UserIdSerializer, FollowListSerializer, BlockListSerializer

class AddFriend(APIView):
    queryset = Friend.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = AddFriendSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        from_user = get_object_or_404(User,id=request.user.id)
        to_user = get_object_or_404(User, id=request.data['to_user'])
        try:
            obj=Friend.objects.add_friend(from_user=from_user, to_user=to_user)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("request has been sent")}, status=status.HTTP_200_OK)

class AcceptFriend(APIView):
    queryset = Friend.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FriendshipRequestIdSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        obj = get_object_or_404(request.user.friendship_requests_received, id=request.data['friend_request_id'])
        try:
            obj.accept()
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("request accepted")}, status=status.HTTP_200_OK)

class RejectFriend(APIView):
    queryset = Friend.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FriendshipRequestIdSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        obj = get_object_or_404(request.user.friendship_requests_received, id=request.data['friend_request_id'])
        try:
            obj.reject()
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("request rejected")}, status=status.HTTP_200_OK)

class CancelFriend(APIView):
    queryset = Friend.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FriendshipRequestIdSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        obj = get_object_or_404(request.user.friendship_requests_sent, id=request.data['friend_request_id'])
        try:
            obj.cancel()
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("request cancelled")}, status=status.HTTP_200_OK)

class FriendRequestList(APIView):
    queryset = FriendshipRequest.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FriendRequestListSerializer

    def get(self, request):
        friendship_requests = Friend.objects.requests(request.user)
        serialized_data = self.serializer_class(friendship_requests, many=True).data
        return Response(serialized_data)
    
# class FriendRequestListReject(APIView):
#     queryset = FriendshipRequest.objects.all()
#     permission_classes  = [IsAuthenticated]
#     serializer_class = FriendRequestListSerializer

#     def get(self, request):
#         friendship_requests = Friend.objects.rejected_requests(request.user)
#         serialized_data = self.serializer_class(friendship_requests, many=True).data
#         return Response(serialized_data)

class FriendRequestDetail(APIView):
    queryset = FriendshipRequest.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FriendshipRequestIdSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  
        friendship_requests = get_object_or_404(FriendshipRequest, id=request.data['friend_request_id'])
        return Response(FriendRequestListSerializer(friendship_requests).data)
    
class Followers(APIView):
    queryset = Follow.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FollowListSerializer

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        try:
            followers = Follow.objects.followers(user)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        serialized_data = self.serializer_class(followers, many=True).data
        return Response(serialized_data)
    
class Following(APIView):
    queryset = Follow.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = FollowListSerializer

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        try:
            following = Follow.objects.following(user)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        serialized_data = self.serializer_class(following, many=True).data
        return Response(serialized_data)
    
class AddFollower(APIView):
    queryset = Follow.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = UserIdSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        followee = get_object_or_404(User, id=request.data['id'])
        follower = request.user
        try:
            Follow.objects.add_follower(follower, followee)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("follower added")}, status=status.HTTP_200_OK)

class RemoveFollower(APIView):
    queryset = Follow.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = UserIdSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        followee = get_object_or_404(User, id=request.data['id'])
        follower = request.user
        try:
            Follow.objects.remove_follower(follower, followee)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("follower removed")}, status=status.HTTP_200_OK)

class BlockingList(APIView):
    queryset = Block.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = BlockListSerializer

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        try:
            block = Block.objects.blocked(user)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        serialized_data = self.serializer_class(block, many=True).data
        return Response(serialized_data)

class BlockersList(APIView):
    queryset = Block.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = BlockListSerializer

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        try:
            block = Block.objects.blocking(user)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        serialized_data = self.serializer_class(block, many=True).data
        return Response(serialized_data)

    
class AddBlock(APIView):
    queryset = Block.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = UserIdSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        blocked = get_object_or_404(User, id=request.data['id'])
        blocker = request.user
        try:
            Block.objects.add_block(blocker, blocked)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("user blocked")}, status=status.HTTP_200_OK)
    
class RemoveBlock(APIView):
    queryset = User.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = UserIdSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        blocked = get_object_or_404(User, id=request.data['id'])
        blocker = request.user
        try:
            Block.objects.remove_block(blocker, blocked)
        except Exception as ex:
            return Response(data={'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(data={"message":_("remove block user")}, status=status.HTTP_200_OK)