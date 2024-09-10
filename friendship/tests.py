from django.test import TestCase
from django.test import Client
from django.urls import reverse
from dj_rest_auth.utils import jwt_encode
from friendship.models import FriendshipRequest
from django.contrib.auth import get_user_model

class SendFriendRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token 
                        }   
        self.url = reverse('send_friend_request')
        friend = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123") 
        self.data = {
                        "to_user": str(friend.id)          
                    }  
    
    def test_friend_request_send_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_friend_request_send_successfully => pass")
    
    def test_friend_request_send_failed_invalid_user_id(self):
        self.data['to_user'] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 400)
        print(" test_friend_request_send_failed_invalid_user_id => pass")

    def test_friend_request_send_failed_invalid_token_or_without_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_friend_request_send_failed_invalid_token_or_without_token => pass")

class AccetpFriendRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('accept_friend_request')
        self.friend = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123")
        access_token, refresh_token = jwt_encode(self.friend)
        friend_token = str(access_token)
        self.friend_request_id=FriendshipRequest.objects.create(from_user=self.friend, to_user=self.user).id
        self.client.post(reverse('send_friend_request'), {
                        "to_user": str(self.friend.id)          
                    }, format='json', **{"HTTP_AUTHORIZATION": "Bearer " + friend_token})
        self.data = {
                        "friend_request_id": self.friend_request_id            
                    }
        
    def test_accept_friend_request_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_accept_friend_request_successfully => pass")
    
    def test_accept_friend_request_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_accept_friend_request_failed_invalid_token => pass")

    def test_accept_friend_request_failed_invalid_requested_friend_request_id(self):
        self.data['friend_request_id'] = 0
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_accept_friend_request_failed_invalid_requested_friend_request_id => pass")
        
class RejectFriendRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('reject_friend_request')
        self.friend = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123")
        access_token, refresh_token = jwt_encode(self.friend)
        friend_token = str(access_token)
        self.friend_request_id=FriendshipRequest.objects.create(from_user=self.friend, to_user=self.user).id
        self.client.post(reverse('send_friend_request'), {
                        "to_user": str(self.friend.id)          
                    }, format='json', **{"HTTP_AUTHORIZATION": "Bearer " + friend_token})
        self.data = {
                        "friend_request_id": self.friend_request_id           
                    }
        
    def test_reject_friend_request_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_accept_friend_request_successfully => pass")
    
    def test_reject_friend_request_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_reject_friend_request_failed_invalid_token => pass")

    def test_reject_friend_request_failed_invalid_requested_friend_request_id(self):
        self.data['friend_request_id'] = 0
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_reject_friend_request_failed_invalid_requested_friend_request_id => pass")

class CancelFriendRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)  
        self.url = reverse('cancel_friend_request')
        self.friend = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123")
        access_token, refresh_token = jwt_encode(self.friend)
        friend_token = str(access_token)
        self.friend_request_id=FriendshipRequest.objects.create(from_user=self.friend, to_user=self.user).id
        self.client.post(reverse('send_friend_request'), {
                        "to_user": str(self.friend.id)          
                    }, format='json', **{"HTTP_AUTHORIZATION": "Bearer " + friend_token})
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + friend_token
                        } 
        self.data = {
                        "friend_request_id": self.friend_request_id           
                    }
        
    def test_cancel_friend_request_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        print(self.url)
        self.assertEqual(response.status_code, 200)
        print(" test_cancel_friend_request_successfully => pass")
    
    def test_cancel_friend_request_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_cancel_friend_request_failed_invalid_token => pass")

    def test_cancel_friend_request_failed_invalid_requested_friend_request_id(self):
        self.data['friend_request_id'] = 0
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_cancel_friend_request_failed_invalid_requested_friend_request_id => pass")

class FriendRequestListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token 
                        }   
        self.url = reverse('friend_request_list')
    
    def test_friend_request_list_successfully(self):
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_friend_request_list_successfully => pass")
    
    def test_friend_request_list_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION']=''
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_friend_request_list_failed_invalid_token => pass")

# class RejectFriendRequestListTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
#         self.access_token, self.refresh_token = jwt_encode(self.user)
#         token = str(self.access_token)
#         self.headers = {
#                              "HTTP_AUTHORIZATION": "Bearer " + token 
#                         }   
#         self.url = reverse('friend_request_reject_list')
    
#     def test_reject_friend_request_list_successfully(self):
#         response = self.client.get(self.url, format='json', **self.headers)
#         self.assertEqual(response.status_code, 200)
#         print(" test_reject_friend_request_failed_invalid_data => pass")
    
#     def test_reject_friend_request_list_failed_invalid_token(self):
#         response = self.client.get(self.url, format='json', **self.headers)
#         self.assertEqual(response.status_code, 401)
#         print(" test_reject_friend_request_failed_invalid_token => pass")

class FriendRequestDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token 
                        }   
        self.url = reverse('friend_request_detail')
        self.friend = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123")
        access_token, refresh_token = jwt_encode(self.friend)
        friend_token = str(access_token)
        self.friend_request_id=FriendshipRequest.objects.create(from_user=self.friend, to_user=self.user).id
        self.client.post(reverse('send_friend_request'), {
                        "to_user": str(self.friend.id)          
                    }, format='json', **{"HTTP_AUTHORIZATION": "Bearer " + friend_token})
        self.data = {
                        "friend_request_id": self.friend_request_id   
                    }
        
    def test_friend_request_detail_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_reject_friend_request_failed_invalid_data => pass")
    
    def test_friend_request_detail_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION']=''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_reject_friend_request_failed_invalid_data => pass")
    
    def test_friend_request_detail_failed_invalid_requested_friend_request_id(self):
        self.data['friend_request_id'] = 0
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_friend_request_detail_failed_invalid_requested_friend_request_id => pass")

class FollowerListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('follwer_list')
    
    def test_follower_list_successfully(self):
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_follower_list_successfully => pass")
    
    def test_follower_list_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION']=''
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_follower_list_failed_invalid_token => pass")

class FollowingListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('follwing_list')
    
    def test_following_list_successfully(self):
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_following_list_successfully => pass")
    
    def test_following_list_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION']=''
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_following_list_failed_invalid_token => pass")

class AddFollowerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('add_follower')
        self.id = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123").id
        self.data = {
                        "id": self.id    
                    }
    
    def test_add_follower_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_add_follower_successfully => pass")
    
    def test_add_follower_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_add_follower_failed_invalid_token => pass")

    def test_add_follower_failed_invalid_requested_user_id(self):
        self.data['id'] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_add_follower_failed_invalid_requested_user_id => pass")

class RemoveFollowerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('remove_follower')
        self.id = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123").id
        self.data = {
                        "id": self.id        
                    }
    
    def test_remove_follower_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_remove_follower_successfully => pass")
    
    def test_remove_follower_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_remove_follower_failed_invalid_token => pass")

    def test_remove_follower_failed_invalid_requested_user_id(self):
        self.data['id'] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_remove_follower_failed_invalid_requested_user_id => pass")

class BlockerListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('blocker_list')
    
    def test_blocker_list_successfully(self):
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_blocker_list_successfully => pass")
    
    def test_blocker_list_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_blocker_list_failed_invalid_token => pass")

class BlockingListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('blocking_list')
    
    def test_blocking_list_successfully(self):
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_blocking_list_successfully => pass")
    
    def test_blocking_list_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.get(self.url, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_blocking_list_failed_invalid_token => pass")

class AddBlockTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('add_block')
        self.id = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123").id
        self.data = {
                        "id": self.id        
                    }
    
    def test_add_block_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_add_block_successfully => pass")
    
    def test_add_block_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_add_block_failed_invalid_token => pass")

    def test_add_block_failed_invalid_requested_user_id(self):
        self.data['id'] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_add_block_failed_invalid_requested_user_id => pass")

class RemoveBlockTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email="user1@gmail.com", full_name="user1 user1", password="User1@123")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        token = str(self.access_token)
        self.headers = {
                             "HTTP_AUTHORIZATION": "Bearer " + token
                        }   
        self.url = reverse('remove_block')
        self.id = get_user_model().objects.create_user(email="user2@gmail.com", full_name="user2 user2", password="User2@123").id
        self.data = {
                        "id": self.id        
                    }
    
    def test_remove_block_successfully(self):
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 200)
        print(" test_remove_block_successfully => pass")
    
    def test_remove_block_failed_invalid_token(self):
        self.headers['HTTP_AUTHORIZATION'] = ''
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 401)
        print(" test_remove_block_failed_invalid_token => pass")

    def test_remove_block_failed_invalid_requested_user_id(self):
        self.data['id'] = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.post(self.url, self.data, format='json', **self.headers)
        self.assertEqual(response.status_code, 404)
        print(" test_remove_block_failed_invalid_requested_user_id => pass")