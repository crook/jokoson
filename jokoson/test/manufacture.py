from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers
from jokoson.db import models
from jokoson.test.data import TestData


class UserCreateManufactureTest(APITestCase):
    """
    Create a manufacture.
    """

    def test_create_manufacture(self):
        td_Hako = TestData.manufacture['Hako']
        response = self.client.post(reverse('manufacture-list'), td_Hako)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteManufactureTest(APITestCase):
    """
    Non-admin user can not delete manufacture.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_hako = TestData.manufacture['Hako']
        self.client.post(reverse('manufacture-list'), td_hako)

        self.client.logout()

    def test_delete_manufacture(self):
        td_hako = TestData.manufacture['Hako']
        manufacture = models.Manufacture.objects.get(name=td_hako['name'])
        response = self.client.delete(
            reverse('manufacture-detail', args=[manufacture.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListManufactureTest(APITestCase):
    """
    Non-admin user can list manufacture.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_hako = TestData.manufacture['Hako']
        self.hako = models.Manufacture.objects.create(**td_hako)
        self.client.logout()

    def test_list_manufacture(self):
        response = self.client.get(reverse('manufacture-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        td_hako = TestData.manufacture['Hako']
        for k, v in td_hako.items():
            self.assertEqual(response.data[0][k], v)

    def test_get_manufacture_detail(self):
        response = self.client.get(
            reverse('manufacture-detail', args=[self.hako.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        td_hako = TestData.manufacture['Hako']
        for k, v in td_hako.items():
            self.assertEqual(response.data[k], v)

    def test_list_manufacture_with_name_filter(self):
        td_hako = TestData.manufacture['Hako']
        response = self.client.get(reverse('manufacture-list'),
                                   {'name': td_hako['name']})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for k, v in td_hako.items():
            self.assertEqual(response.data[0][k], v)


class AdminCreateManufactureTest(APITestCase):
    """
    Create a manufacture with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

    def test_create_manufacture_with_admin_login(self):
        td_hako = TestData.manufacture['Hako']
        response = self.client.post(reverse('manufacture-list'), td_hako)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_manufacture_with_none_parameter(self):
        # Haulotte has no cellphone
        td_haulotte = TestData.manufacture['Haulotte']
        response = self.client.post(reverse('manufacture-list'), td_haulotte)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AdminDeleteManufactureTest(APITestCase):
    """
    Delete a manufacture with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_hako = TestData.manufacture['Hako']
        self.client.post(reverse('manufacture-list'), td_hako)

    def test_create_manufacture_with_admin_login(self):
        td_hako = TestData.manufacture['Hako']
        manufacture = models.Manufacture.objects.get(name=td_hako['name'])
        response = self.client.delete(
            reverse('manufacture-detail', args=[manufacture.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListManufactureTest(APITestCase):
    """
    List a manufacture and manufacture detail with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_hako = TestData.manufacture['Hako']
        self.manufacture = models.Manufacture.objects.create(**td_hako)

    def test_list_manufacture_with_admin_login(self):
        response = self.client.get(reverse('manufacture-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        td_hako = TestData.manufacture['Hako']
        for k, v in td_hako.items():
            self.assertEqual(response.data[0][k], v)

    def test_get_manufacture_detail_with_admin_login(self):
        response = self.client.get(
            reverse('manufacture-detail', args=[self.manufacture.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        td_hako = TestData.manufacture['Hako']
        for k, v in td_hako.items():
            self.assertEqual(response.data[k], v)

    def test_list_manufacture_with_name_filter(self):
        td_hako = TestData.manufacture['Hako']
        response = self.client.get(reverse('manufacture-list'),
                                   {'name': td_hako['name']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for k, v in td_hako.items():
            self.assertEqual(response.data[0][k], v)


class AdminUpdateManufactureTest(APITestCase):
    """
    Update manufacture information with admin privilege
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_hako = TestData.manufacture['Hako']

        self.manufacture = serializers.ManufactureSerializer(
            models.Manufacture.objects.create(**td_hako)).data
        self.manufacture.update(
            {'city': 'Changed', 'cell_phone': "Changed"})

    def test_update_manufacture_with_admin_login(self):
        response = self.client.put(
            reverse('manufacture-detail',
                    args=[self.manufacture['id']]),
            self.manufacture)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        td_hako = TestData.manufacture['Hako']
        for key in td_hako.keys():
            self.assertEqual(response.data[key], self.manufacture[key])
