import copy

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import models
from jokoson.test.data import TestData




class AdminCreateOrderTest(APITestCase):
    """
    Create a order with the admin privilege.
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

    def test_create_order_with_admin_login(self):
        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['john']['username']
        response = self.client.post(reverse('order-list'), order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_other_tenant_order_with_admin_login(self):
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        response = self.client.post(reverse('order-list'), order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteOrderTest(APITestCase):
    """
    Delete a order with the admin privilege.
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
        self.client.post(reverse('equip-list'), self.equip)

        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['john']['username']
        self.client.post(reverse('order-list'), order)

    def test_delete_order_with_admin_login(self):
        equip = models.Equip.objects.get(sn=self.equip['sn'])
        order = models.Order.objects.get(equip_id=equip.id)
        response = self.client.delete(
            reverse('order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListOrderTest(APITestCase):
    """
    List a order and order detail with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        self.equip_1 = TestData.equip['star-10-1111111']
        self.client.post(reverse('equip-list'), self.equip_1)

        self.equip_2 = TestData.equip['star-10-2222222']
        self.client.post(reverse('equip-list'), self.equip_2)

        order_1 = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order_1['tenant'] = TestData.user['john']['username']
        self.client.post(reverse('order-list'), order_1)

        order_2 = TestData.orders['star-10-2222222']
        # Must set the tenant of the order
        order_2['tenant'] = TestData.user['john']['username']
        self.client.post(reverse('order-list'), order_2)

    def test_list_order_with_admin_login(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_order_detail_with_admin_login(self):
        equip = models.Equip.objects.get(sn=self.equip_1['sn'])
        order = models.Order.objects.get(equip_id=equip.id)
        response = self.client.get(
            reverse('order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_1 = TestData.orders['star-10-1111111']
        for k, v in order_1.items():
            if k not in ('tenant', 'equip_sn'):
                self.assertEqual(response.data[k], v)

    def test_list_order_with_name_filter_with_admin_login(self):
        response = self.client.get(reverse('order-list'),
                                   {'equip_sn': self.equip_1['sn']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        order_1 = TestData.orders['star-10-1111111']
        for k, v in order_1.items():
            if k not in ('tenant', 'equip_sn'):
                self.assertEqual(response.data[0][k], v)


class AdminUpdateOrderTest(APITestCase):
    """
    Update order information with admin privilege
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

        self.order = copy.deepcopy(TestData.orders['star-10-1111111'])
        # Must set the tenant of the order
        self.order['tenant'] = TestData.user['john']['username']
        response = self.client.post(reverse('order-list'), self.order)
        self.order.update(
            {
                'endtime': '2019-10-30T12:38:57Z',
                'id': response.data['id'],
            })

    def test_update_order_with_admin_login(self):
        response = self.client.put(
            reverse('order-detail', args=[self.order['id']]), self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in self.order.items():
            if k not in ('tenant', 'equip_sn'):
                self.assertEqual(response.data[k], v)


class UserCreateOrderWithoutLoginTest(APITestCase):
    """
    Create a order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        equip = TestData.equip['star-10-1111111']
        self.client.post(reverse('equip-list'), equip)

        self.client.logout()

    def test_create_order(self):
        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        response = self.client.post(reverse('order-list'), order)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteOrderWithoutLoginTest(APITestCase):
    """
    Non-admin user can not delete order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        self.equip = TestData.equip['star-10-1111111']
        self.client.post(reverse('equip-list'), self.equip)

        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

        self.client.logout()

    def test_delete_order(self):
        equip = models.Equip.objects.get(sn=self.equip['sn'])
        order = models.Order.objects.get(equip_id=equip.id)
        response = self.client.delete(
            reverse('order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListOrderWithoutLoginTest(APITestCase):
    """
    Non-admin user can list order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        category = TestData.category['star-10']
        self.category = models.Category.objects.create(**category)

        vendor = TestData.vendor['Hako']
        self.vendor = models.Vendor.objects.create(**vendor)

        self.equip = TestData.equip['star-10-1111111']
        self.client.post(reverse('equip-list'), self.equip)

        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

        self.client.logout()

    def test_list_order(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserCreateOrderTest(APITestCase):
    """
    Create a order.
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

        # Create a non-admin user Mike and then login again
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.client.login(**mike)

    def test_create_order(self):
        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        response = self.client.post(reverse('order-list'), order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserDeleteOrderTest(APITestCase):
    """
    Non-admin user can not delete order.
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
        self.client.post(reverse('equip-list'), self.equip)

        self.client.logout()

        # Create a non-admin user Mike and then login again
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.client.login(**mike)

        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)
        response = self.client.get(reverse('order-list'))
        print(response)

    def test_delete_order(self):
        equip = models.Equip.objects.get(sn=self.equip['sn'])
        order = models.Order.objects.get(equip_id=equip.id)
        response = self.client.delete(
            reverse('order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserListOrderTest(APITestCase):
    """
    Non-admin user can list order.
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
        self.client.post(reverse('equip-list'), self.equip)

        order = TestData.orders['star-10-1111111']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['john']['username']
        self.client.post(reverse('order-list'), order)

        self.client.logout()

        # Create a non-admin user Mike and then login again
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.client.login(**mike)

        order = TestData.orders['star-10-2222222']
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

    def test_list_order(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        order = TestData.orders['star-10-1111111']
        for k, v in order.items():
            if k not in ('tenant', 'equip_sn'):
                self.assertEqual(response.data[0][k], v)

    def test_get_order_detail(self):
        equip = models.Equip.objects.get(sn=self.equip['sn'])
        order_xx = models.Order.objects.get(equip_id=equip.id)
        response = self.client.get(
            reverse('order-detail', args=[order_xx.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order = TestData.orders['star-10-1111111']
        for k, v in order.items():
            if k not in ('tenant', 'equip_sn'):
                self.assertEqual(response.data[k], v)

    def test_list_order_with_name_filter(self):
        response = self.client.get(reverse('order-list'),
                                   {'equip_sn': self.equip['sn']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        order = TestData.orders['star-10-1111111']
        for k, v in order.items():
            if k not in ('tenant', 'equip_sn'):
                self.assertEqual(response.data[0][k], v)
