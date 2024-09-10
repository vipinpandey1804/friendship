from django.urls import path
from rest_framework.routers import DefaultRouter
from friendship.views import *

router=DefaultRouter()

urlpatterns = router.urls
urlpatterns += [
    path('send-friend-request/', AddFriend.as_view(), name='send_friend_request'),
    path('accept-friend-request/', AcceptFriend.as_view(), name='accept_friend_request'),
    path('reject-friend-request/', RejectFriend.as_view(), name='reject_friend_request'),
    path('cancel-friend-request/', CancelFriend.as_view(), name='cancel_friend_request'),
    path('friend-request-list/', FriendRequestList.as_view(), name='friend_request_list'),
    # path('friend-request-reject-list', FriendRequestListReject.as_view(), name='friend_request_reject_list'),
    path('friend-request-detail/', FriendRequestDetail.as_view(), name='friend_request_detail'),
    path('follower-list/', Followers.as_view(), name='follower_list'),
    path('following-list/', Following.as_view(), name='following_list'),
    path('add-follower/', AddFollower.as_view(), name='add_follower'),
    path('remove-follower/', RemoveFollower.as_view(), name='remove_follower'),
    path('blocker-list/', BlockersList.as_view(), name='blocker_list'),
    path('blocking-list/', BlockingList.as_view(), name='blocking_list'),
    path('add-block/', AddBlock.as_view(), name='add_block'),
    path('remove-block/', RemoveBlock.as_view(), name='remove_block'),    
]