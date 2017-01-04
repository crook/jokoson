from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers
from jokoson.test.data import TestData


class AdminCreateUserTest(APITestCase):
    """
    Create a non-admin user with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

    def test_create_user_with_admin_login(self):
        mike = TestData.user['mike']
        response = self.client.post(reverse('user-list'), mike)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminListUserTest(APITestCase):
    """
    List the user and the user detail with admin privilege
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_mike = TestData.user['mike']
        self.mike = User.objects.create(**td_mike)

    def test_list_user_with_admin_login(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_detail_with_admin_login(self):
        td_mike = TestData.user['mike']
        response = self.client.get(reverse('user-detail', args=[self.mike.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in td_mike:
            if key != 'password':
                self.assertEqual(response.data[key], td_mike[key])

    def test_list_user_with_name_filter(self):
        td_mike = TestData.user['mike']
        user = {'username': td_mike['username']}
        response = self.client.get(reverse('user-list'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for key in TestData.user['mike']:
            if key != 'password':
                self.assertEqual(response.data[0][key], td_mike[key])


class AdminUpdateUserTest(APITestCase):
    """
    Update another user's content with admin privilege
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_mike = TestData.user['mike']
        self.mike = serializers.TenantSerializer(
            User.objects.create(**td_mike)).data
        self.mike.update({'first_name': 'Changed'}, )

    def test_update_user_with_admin_login(self):
        response = self.client.put(
            reverse('user-detail', args=[self.mike['id']]), self.mike)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Changed')


class AdminDeleteUserTest(APITestCase):
    """
    Delete another user account with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_mike = TestData.user['mike']
        self.mike = User.objects.create(**td_mike)

    def test_delete_user_with_admin_login(self):
        response = self.client.delete(
            reverse('user-detail', args=[self.mike.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminLoginTest(APITestCase):
    """
    Login with the admin privilege
    """

    def setUp(self):
        self.john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**self.john)

    def test_admin_login(self):
        self.assertTrue(
            self.client.login(**self.john))


class AdminLogoutTest(APITestCase):
    """
    Admin logout
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

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
        self.mike = TestData.user['mike']

    def test_create_user(self):
        response = self.client.post(reverse('user-list'), self.mike)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginUserTest(APITestCase):
    """
    Create a non-admin user and then login
    """

    def setUp(self):
        self.mike = TestData.user['mike']

        self.client.post(reverse('user-list'), self.mike)

    def test_login_user(self):
        self.assertTrue(
            self.client.login(**self.mike))


class UserListUserTest(APITestCase):
    """
    Check if the non-admin user can only list himself.
    """

    def setUp(self):
        self.users = [
            TestData.user['john'],
            TestData.user['mike'],
        ]
        for user in self.users:
            self.client.post(reverse('user-list'), user)

        self.mike = TestData.user['mike']
        self.client.login(**self.mike)

    def test_list_user(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for key in TestData.user['mike']:
            if key != 'password':
                self.assertEqual(response.data[0][key], self.mike[key])

    def test_list_user_with_name_filter(self):
        user = {'username': self.mike['username']}
        response = self.client.get(reverse('user-list'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for key in self.mike:
            if key != 'password':
                self.assertEqual(response.data[0][key], self.mike[key])

    def test_list_user_with_other_name_filter(self):
        td_john = TestData.user['john']
        user = {'username': td_john['username']}
        response = self.client.get(reverse('user-list'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)


class UserListUserWithoutLoginTest(APITestCase):
    """
    No user will be listed without the account login.
    """

    def setUp(self):
        self.users = [
            TestData.user['john'],
            TestData.user['mike'],
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
        td_mike = TestData.user['mike']

        self.client.post(reverse('user-list'), td_mike)

        self.client.login(**td_mike)

        self.mike = serializers.TenantSerializer(
            User.objects.get(username=td_mike['username'])).data
        self.mike.update({'first_name': 'Changed'}, )

    def test_can_update_user(self):
        response = self.client.put(reverse('user-detail',
                                           args=[self.mike['id']]),
                                   self.mike)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.mike['first_name'])


class UserDeleteUserTest(APITestCase):
    """
    Non-admin user can delete himself.
    """

    def setUp(self):
        self.users = [
            TestData.user['john'],
            TestData.user['mike'],
        ]

        for user in self.users:
            self.client.post(reverse('user-list'), user)

        self.mike = TestData.user['mike']
        self.client.login(**self.mike)

    def test_delete_user(self):
        user = User.objects.get(username=self.mike['username'])
        response = self.client.delete(
            reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user(self):
        td_john = TestData.user['john']
        user = User.objects.get(username=td_john['username'])
        response = self.client.delete(
            reverse('user-detail', args=[user.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
