from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers
from jokoson.db import models
from jokoson.test.data import TestData


class UserCreateVendorTest(APITestCase):
    """
    Create a vendor.
    """

    def test_create_vendor(self):
        Hako = TestData.vendor['Hako']
        response = self.client.post(reverse('vendor-list'), Hako)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteVendorTest(APITestCase):
    """
    Non-admin user can not delete vendor.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        hako = TestData.vendor['Hako']
        self.client.post(reverse('vendor-list'), hako)

        self.client.logout()

    def test_delete_category(self):
        hako = TestData.vendor['Hako']
        vendor = models.Vendor.objects.get(name=hako['name'])
        response = self.client.delete(
            reverse('vendor-detail', args=[vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListVendorTest(APITestCase):
    """
    Non-admin user can list vendor.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        hako = TestData.vendor['Hako']
        self.hako = models.Vendor.objects.create(**hako)
        self.client.logout()

    def test_list_vendor(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        hako = TestData.vendor['Hako']
        for k, v in hako.items():
            self.assertEqual(response.data[0][k], v)

    def test_get_vendor_detail(self):
        response = self.client.get(
            reverse('vendor-detail', args=[self.hako.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        hako = TestData.vendor['Hako']
        for k, v in hako.items():
            self.assertEqual(response.data[k], v)

    def test_list_vendor_with_name_filter(self):
        hako = TestData.vendor['Hako']
        response = self.client.get(reverse('vendor-list'),
                                   {'name': hako['name']})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for k, v in hako.items():
            self.assertEqual(response.data[0][k], v)


class AdminCreateVendorTest(APITestCase):
    """
    Create a vendor with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

    def test_create_vendor_with_admin_login(self):
        hako = TestData.vendor['Hako']
        response = self.client.post(reverse('vendor-list'), hako)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteVendorTest(APITestCase):
    """
    Delete a vendor with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        hako = TestData.vendor['Hako']
        self.client.post(reverse('vendor-list'), hako)

    def test_create_vendor_with_admin_login(self):
        hako = TestData.vendor['Hako']
        vendor = models.Vendor.objects.get(name=hako['name'])
        response = self.client.delete(
            reverse('vendor-detail', args=[vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListVendorTest(APITestCase):
    """
    List a vendor and vendor detail with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        hako = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**hako)

    def test_list_vendor_with_admin_login(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        hako = TestData.vendor['Hako']
        for k, v in hako.items():
            self.assertEqual(response.data[0][k], v)

    def test_get_vendor_detail_with_admin_login(self):
        response = self.client.get(
            reverse('vendor-detail', args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        hako = TestData.vendor['Hako']
        for k, v in hako.items():
            self.assertEqual(response.data[k], v)

    def test_list_vendor_with_name_filter(self):
        hako = TestData.vendor['Hako']
        response = self.client.get(reverse('vendor-list'),
                                   {'name': hako['name']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        hako = TestData.vendor['Hako']
        for k, v in hako.items():
            self.assertEqual(response.data[0][k], v)


class AdminUpdateVendorTest(APITestCase):
    """
    Update vendor information with admin privilege
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        hako = TestData.vendor['Hako']

        self.vendor = serializers.VendorSerializer(
            models.Vendor.objects.create(**hako)).data
        self.vendor.update(
            {'city': 'Changed', 'cell_phone': "Changed"})

    def test_update_vendor_with_admin_login(self):
        response = self.client.put(
            reverse('vendor-detail', args=[self.vendor['id']]), self.vendor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        hako = TestData.vendor['Hako']
        for key in hako.keys():
            self.assertEqual(response.data[key], self.vendor[key])
