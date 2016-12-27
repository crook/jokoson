from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers
from jokoson.db import models
from jokoson.test.data import TestData


class AdminCreateEquipTest(APITestCase):
    """
    Create a equip with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        star_10 = TestData.category['star-10']
        self.category = models.Category.objects.create(**star_10)

        hako = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**hako)

    def test_create_equip_with_admin_login(self):
        equip = TestData.equip['star-10-1111111']
        response = self.client.post(reverse('equip-list'), equip)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteEquipTest(APITestCase):
    """
    Delete a equip with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        star_10 = TestData.category['star-10']
        self.category = models.Category.objects.create(**star_10)

        hako = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**hako)

        self.equip = TestData.equip['star-10-1111111']
        self.client.post(reverse('equip-list'), self.equip)

    def test_delete_equip_with_admin_login(self):
        equip = models.Equip.objects.get(sn=self.equip['sn'])
        response = self.client.delete(
            reverse('equip-detail', args=[equip.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListEquipTest(APITestCase):
    """
    List a equip and equip detail with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        star_10 = TestData.category['star-10']
        self.category = models.Category.objects.create(**star_10)

        hako = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**hako)

        self.equip = TestData.equip['star-10-1111111']
        response = self.client.post(reverse('equip-list'), self.equip)
        self.equip.update({'id': response.data['id']})

    def test_list_equip_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for k, v in self.equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[0][k], v)

    def test_get_equip_detail_with_admin_login(self):
        response = self.client.get(
            reverse('equip-detail', args=[self.equip['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for k, v in self.equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[k], v)

    def test_list_equip_with_name_filter_with_admin_login(self):
        response = self.client.get(reverse('equip-list'),
                                   {'model': self.equip['model']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for k, v in self.equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[0][k], v)


class AdminUpdateEquipTest(APITestCase):
    """
    Update equip information with admin privilege
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        self.equip = TestData.equip['star-10-1111111']
        response = self.client.post(reverse('equip-list'), self.equip)
        self.equip.update(
            {
                'sn': 'Changed',
                'description': "Changed",
                'id': response.data['id'],
            })

    def test_update_equip_with_admin_login(self):
        response = self.client.put(
            reverse('equip-detail', args=[self.equip['id']]), self.equip)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for k, v in self.equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[k], v)


class UserCreateEquipTest(APITestCase):
    """
    Create a equip.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        self.equip = TestData.equip['star-10-1111111']
        self.client.logout()

    def test_create_equip(self):
        response = self.client.post(reverse('equip-list'), self.equip)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteEquipTest(APITestCase):
    """
    Non-admin user can not delete equip.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        equip = TestData.equip['star-10-1111111']
        self.client.post(reverse('equip-list'), equip)
        self.client.logout()

    def test_delete_equip(self):
        sn = TestData.equip['star-10-1111111']['sn']
        equip = models.Equip.objects.get(sn=sn)
        response = self.client.delete(reverse('equip-detail', args=[equip.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListEquipTest(APITestCase):
    """
    Non-admin user can list equip.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        self.equip = TestData.equip['star-10-1111111']
        response = self.client.post(reverse('equip-list'), self.equip)
        self.equip.update({'id': response.data['id']})
        self.client.logout()

    def test_list_equip(self):
        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for k, v in self.equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[0][k], v)

    def test_get_equip_detail(self):
        response = self.client.get(
            reverse('equip-detail', args=[self.equip['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in self.equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[k], v)

    def test_list_equip_with_sn_filter(self):
        equip = TestData.equip['star-10-1111111']
        response = self.client.get(reverse('equip-list'), {'sn': equip['sn']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        for k, v in equip.items():
            if k not in ('category', 'vendor'):
                self.assertEqual(response.data[0][k], v)
