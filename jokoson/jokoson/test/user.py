from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers


class AdminCreateUserTest(APITestCase):
    """
    Create a non-admin user with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            'username': 'mike',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password': 'tysonpassword',
            'email': 'mike.tyson@google.com',
        }

    def test_create_user_with_admin_login(self):
        response = self.client.post(reverse('user-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminListUserTest(APITestCase):
    """
    List the user and the user detail with admin privilege
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike")

    def test_list_user_with_admin_login(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_detail_with_admin_login(self):
        response = self.client.get(reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)

    def test_list_user_with_name_filter(self):
        user_name = 'mike'
        user = {'username': user_name}
        response = self.client.get(reverse('user-list'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], user_name)


class AdminUpdateUserTest(APITestCase):
    """
    Update another user's content with admin privilege
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.data = {
            'username': 'mike',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password': 'tysonpassword',
            'email': 'mike.tyson@google.com',
        }
        self.user = User.objects.create(**self.data)
        self.data = serializers.TenantSerializer(self.user).data
        self.data.update({'first_name': 'Changed'}, )

    def test_update_user_with_admin_login(self):
        response = self.client.put(
            reverse('user-detail', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.data['first_name'])


class AdminDeleteUserTest(APITestCase):
    """
    Delete another user account with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mikey")

    def test_delete_user_with_admin_login(self):
        response = self.client.delete(
            reverse('user-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminLoginTest(APITestCase):
    """
    Login with the admin privilege
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')

    def test_admin_login(self):
        self.assertTrue(
            self.client.login(username='john', password='johnpassword'))


class AdminLogoutTest(APITestCase):
    """
    Admin logout
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_admin_logout(self):
        self.client.logout()

        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)


class UserCreateUserTest(APITestCase):
    """
    Create a non-admin user.
    """

    def setUp(self):
        self.data = {
            'username': 'mike',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password': 'tysonpassword',
            'email': 'mike.tyson@google.com',
            'is_active': True,
        }

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginUserTest(APITestCase):
    """
    Create a non-admin user and then login
    """

    def setUp(self):
        self.data = {
            'username': 'mike',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password': 'tysonpassword',
            'email': 'mike.tyson@google.com',
            'is_active': True,
        }

        self.client.post(reverse('user-list'), self.data)

    def test_login_user(self):
        self.assertTrue(
            self.client.login(username='mike', password='tysonpassword'))


class UserListUserTest(APITestCase):
    """
    Check if the non-admin user can only list himself.
    """

    def setUp(self):
        self.users = [
            {
                'username': 'mike',
                'first_name': 'Mike',
                'last_name': 'Tyson',
                'password': 'tysonpassword',
                'email': 'mike.tyson@google.com',
                'is_active': True,
            },
            {
                'username': 'john',
                'first_name': 'John',
                'last_name': 'Handsome',
                'password': 'johnpassword',
                'email': 'john.handsome@google.com',
                'is_active': True,
            },
        ]
        for user in self.users:
            self.client.post(reverse('user-list'), user)

        self.client.login(username='mike', password='tysonpassword')

    def test_list_user(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual((response.data[0]['username']), 'mike')

    def test_list_user_with_name_filter(self):
        user_name = 'mike'
        user = {'username': user_name}
        response = self.client.get(reverse('user-list'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], user_name)

    def test_list_user_with_other_name_filter(self):
        user_name = 'john'
        user = {'username': user_name}
        response = self.client.get(reverse('user-list'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)


class UserListUserWithoutLoginTest(APITestCase):
    """
    No user will be listed without the account login.
    """

    def setUp(self):
        self.users = [
            {
                'username': 'mike',
                'first_name': 'Mike',
                'last_name': 'Tyson',
                'password': 'tysonpassword',
                'email': 'mike.tyson@google.com',
                'is_active': True,
            },
            {
                'username': 'john',
                'first_name': 'John',
                'last_name': 'Handsome',
                'password': 'johnpassword',
                'email': 'john.handsome@google.com',
                'is_active': True,
            },
        ]
        for user in self.users:
            self.client.post(reverse('user-list'), user)

    def test_list_user_without_login(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)


class UserUpdateUserTest(APITestCase):
    """
    Non-admin could update his profile info.
    """

    def setUp(self):
        self.data = {
            'username': 'mike',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password': 'tysonpassword',
            'email': 'mike.tyson@google.com',
            'is_active': True,
        }

        self.client.post(reverse('user-list'), self.data)

        self.client.login(username='mike', password='tysonpassword')

        self.user = User.objects.get(username='mike')
        self.data = serializers.TenantSerializer(self.user).data
        self.data.update({'first_name': 'Changed'}, )

    def test_can_update_user(self):
        response = self.client.put(
            reverse('user-detail', args=[self.user.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.data['first_name'])


class UserDeleteUserTest(APITestCase):
    """
    Non-admin user can delete himself.
    """

    def setUp(self):
        self.users = [
            {
                'username': 'mike',
                'first_name': 'Mike',
                'last_name': 'Tyson',
                'password': 'tysonpassword',
                'email': 'mike.tyson@google.com',
                'is_active': True,
            },
            {
                'username': 'john',
                'first_name': 'John',
                'last_name': 'Handsome',
                'password': 'johnpassword',
                'email': 'john.handsome@google.com',
                'is_active': True,
            },
        ]

        for user in self.users:
            self.client.post(reverse('user-list'), user)

        self.client.login(username='mike', password='tysonpassword')

    def test_delete_user(self):
        user = User.objects.get(username='mike')
        response = self.client.delete(
            reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user(self):
        user = User.objects.get(username='john')
        response = self.client.delete(
            reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
