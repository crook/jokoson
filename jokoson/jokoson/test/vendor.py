from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers
from jokoson.db import models
from jokoson import exception


class UserCreateVendorTest(APITestCase):
    """
    Create a vendor.
    """

    def setUp(self):
        self.data = {
            'name': 'Hollet',
            'city': 'Paris',
            'cell_phone': '13411111111',
            'office_phone': '13411111111',
            'address': 'No. 222, Seatle',
        }

    def test_create_vendor(self):
        response = self.client.post(reverse('vendor-list'), self.data)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class UserDeleteVendorTest(APITestCase):
    """
    Non-admin user can not delete vendor.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            'name': 'Hollet',
            'city': 'Paris',
            'cell_phone': '13411111111',
            'office_phone': '13411111111',
            'address': 'No. 222, Seatle',
        }
        self.client.post(reverse('vendor-list'), self.data)
        self.client.logout()

    def test_delete_category(self):
        vendor = models.Vendor.objects.get(name='Hollet')
        response = self.client.delete(reverse('vendor-detail', args=[vendor.id]))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class UserListVendorTest(APITestCase):
    """
    Non-admin user can list vendor.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        vendor = {
            'name': 'Hollet',
            'city': 'Paris',
            'cell_phone': '13411111111',
            'office_phone': '13411111111',
            'address': 'No. 222, Seatle',
        }
        self.vendor = models.Vendor.objects.create(**vendor)
        self.client.logout()

    def test_list_vendor(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.vendor.name)

    def test_get_vendor_detail(self):
        response = self.client.get(
            reverse('vendor-detail', args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)

    def test_list_vendor_with_name_filter(self):
        vendor_name = 'Hollet'
        vendor = {'name': vendor_name}
        response = self.client.get(reverse('vendor-list'), vendor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], vendor_name)


class AdminCreateVendorTest(APITestCase):
    """
    Create a vendor with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            'name': 'Hollet',
            'city': 'Paris',
            'cell_phone': '13411111111',
            'office_phone': '13411111111',
            'address': 'No. 222, Seatle',
        }

    def test_create_vendor_with_admin_login(self):
        response = self.client.post(reverse('vendor-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteVendorTest(APITestCase):
    """
    Delete a vendor with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.data = {
            'name': 'Hollet',
            'city': 'Paris',
            'cell_phone': '13411111111',
            'office_phone': '13411111111',
            'address': 'No. 222, Seatle',
        }
        self.client.post(reverse('vendor-list'), self.data)

    def test_create_vendor_with_admin_login(self):
        vendor = models.Vendor.objects.get(name='Hollet')
        response = self.client.delete(
            reverse('vendor-detail', args=[vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListVendorTest(APITestCase):
    """
    List a vendor and vendor detail with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        vendor = {
            'name': 'Hollet',
            'city': 'Paris',
            'cell_phone': '13411111111',
            'office_phone': '13411111111',
            'address': 'No. 222, Seatle',
        }
        self.vendor = models.Vendor.objects.create(**vendor)

    def test_list_vendor_with_admin_login(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.vendor.name)

    def test_get_vendor_detail_with_admin_login(self):
        response = self.client.get(
            reverse('vendor-detail', args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)

    def test_list_vendor_with_name_filter(self):
        vendor_name = 'Hollet'
        vendor = {'name': vendor_name}
        response = self.client.get(reverse('vendor-list'), vendor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], vendor_name)


class AdminUpdateVendorTest(APITestCase):
    """
    Update vendor information with admin privilege
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.vendor = models.Vendor.objects.create(name="Hollet",
                                                   city="Paris",
                                                   cell_phone='13411111111',
                                                   office_phone='12333333333',
                                                   address='No. 222, Seatle')

        self.data = serializers.VendorSerializer(self.vendor).data
        self.data.update(
            {'city': 'Beijing', 'cell_phone': "13422222222"}, )

    def test_update_vendor_with_admin_login(self):
        response = self.client.put(
            reverse('vendor-detail', args=[self.vendor.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], self.data['city'])
        self.assertEqual(response.data['cell_phone'], self.data['cell_phone'])
