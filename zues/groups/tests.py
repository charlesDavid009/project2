from django.test import TestCase
from .models import Group, MyBlog, Message
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

# Create your tests here.
User = get_user_model()


class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="zues", password="somepasssword")
        self.userb = User.objects.create_user(username="mike", password="somepasssw")
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome", description="whatever", owner=self.userb)
        Group.objects.create(group_name="welcome3", description="4 u", owner=self.userb)
        Group.objects.create(group_name="welcome4", description="whatever2", owner=self.user)
        self.current_count = Group.objects.all().count()

    def test_user_created(self):
        self.assertEqual(self.user.username,  "zues")

    def test_group_create(self):
            group = Group.objects.create(
                group_name="Harvard", description="Will never leave", owner_id=self.user.id)
            self.assertEqual(group.id, 7)
            self.assertEqual(group.owner, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepasssword")
        return client

    def get_client2(self):
        client2 = APIClient()
        client2.login(username=self.userb.username, password="somepasssw")
        return client2

    def test_api_login(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepasssword")
        return client

    def test_Group_list(self):
        client = self.get_client()
        response = client.get("/Group/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    def test_group_action_join(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id": 1, "action": "join"})
        #print(response.json())
        report = response.json().get("request")
        self.assertEqual(report, 1)
        self.assertEqual(response.status_code, 200)

    def test_group_action_follow(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id": 2, "action": "follow"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("follower")
        self.assertEqual(likes, 1)

    def test_action_follow(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id": 3, "action": "unfollow"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("follower")
        self.assertEqual(likes, 0)

    def test_action_exit(self):
        client = self.get_client()
        response = client.post("/Group/action", {"id": 4, "action": "exit"})
        self.assertEqual(response.status_code, 200)
        #print(response.json())
        likes = response.json().get("users")
        self.assertEqual(likes, 1)

    def test_create_group(self):
        client = self.get_client()
        data = {"group_name": "Hello Python",
                "descriptions": "Welcome to the santinuary of the lord!", "owner_id": self.user.id}
        response = client.post("/Group/create", data)
        response_data = response.json()
        new_id = response_data.get("id")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.current_count + 1, new_id)
        #print(response.json())


    def test_delete_group(self):
        client = self.get_client2()
        response = client.delete("/Group/2/delete")
        data = response.json()
        _id = data.get("id")
        self.assertNotEqual(_id, 2)
        self.assertEqual(response.status_code, 201)

    def test_unathorized_delete_blog(self):
        client = self.get_client()
        response = client.delete("/Group/3/delete")
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 3)
        self.assertEqual(response.status_code, 401)
