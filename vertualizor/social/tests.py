from rest_framework.test import APIClient
from django.test import TestCase

# Create your tests here.
# run ./manage.py test to test.
from django.contrib.auth import get_user_model
from .models import Tweet
User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='IamANewUser', password='newPassWord')
        Tweet.objects.create(content='first Tweet.', user=self.user)
        Tweet.objects.create(content='second Tweet.', user=self.user)
        Tweet.objects.create(content='third Tweet.', user=self.user)
        # current number of tweets.
        self.currentCount = Tweet.objects.all().count()

    def test_user_create(self):
        user = User.objects.get(username='IamANewUser')
        self.assertEqual(self.user.username, 'IamANewUser')

    def test_post_create(self):
        newTweet = Tweet.objects.create(content='new tweet.', user=self.user)
        self.assertEqual(newTweet.id, 4)
        self.assertEqual(newTweet.user, self.user)
        self.assertEqual(newTweet.content, 'new tweet.')

    def get_client(self):
      #     test_api_login
        client = APIClient()
        client.login(username=self.user.username, password='newPassWord')
        return client

    def test_posts_list(self):
        client = self.get_client()
        response = client.get('/posts/')
      #   print(response, response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_actions_like_and_unlike(self):
        client = self.get_client()
        id_value = 1
        client.post('/posts/actions/', {'id': id_value, 'action': 'like'})
        response = client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        for i in response.json():
            if i.get('id') == id_value:
                self.assertEqual(len(i.get('like')), 1)
        client.post('/posts/actions/', {'id': id_value, 'action': 'unlike'})
        response = client.get('/posts/')
        for i in response.json():
            if i.get('id') == id_value:
                self.assertEqual(len(i.get('like')), 0)

    def test_actions_reTweet(self):
        client = self.get_client()
        id_value = 1
        postResponse = client.post(
            '/posts/actions/', {'id': id_value, 'action': 'retweet'})
        response = client.get('/posts/')
        self.assertEqual(postResponse.status_code, 201)
        self.assertTrue(postResponse.json().get('is_retweet'))
        # to make sure that it is a new tweet should have diffrent id.
        self.assertNotEqual(id_value, postResponse.json().get("id"))
        print(self.currentCount, postResponse.json().get("id"))
        # the new tweet should have an id = prevuse number of tweets +1
        self.assertEqual(self.currentCount+1, postResponse.json().get("id"))
