import copy
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.test.data import TestData


class AdminCreateOrderTest(APITestCase):
    """
    Create a order with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112104'])
        self.client.post(reverse('equip-list'), equip)

        equip2 = copy.deepcopy(TestData.equip['ME 112108'])
        self.client.post(reverse('equip-list'), equip2)

    def test_create_order_with_admin_login(self):
        order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['john']['username']
        response = self.client.post(reverse('order-list'), order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['equips']), 1)
        self.assertEqual(response.data['equips'][0]['status'], 1)

    def test_create_order_with_admin_login_with_multiple_equip(self):
        order = copy.deepcopy(TestData.orders['ME 112104-112108'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['john']['username']
        response = self.client.post(reverse('order-list'), order)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['equips']), 2)
        self.assertEqual(response.data['equips'][0]['status'], 1)
        self.assertEqual(response.data['equips'][0]['sn'], order['equips'][0])
        self.assertEqual(response.data['equips'][1]['status'], 1)
        self.assertEqual(response.data['equips'][1]['sn'], order['equips'][1])

    def test_create_other_tenant_order_with_admin_login(self):
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        order = copy.deepcopy(TestData.orders['ME 112104'])
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

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112104'])
        self.client.post(reverse('equip-list'), equip)

        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 112104`
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

    def test_delete_order_with_admin_login(self):
        response = self.client.get(reverse('order-list'))
        order = response.data[0]
        response = self.client.delete(
            reverse('order-detail', args=[order['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListOrderTest(APITestCase):
    """
    List a order and order detail with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), equip)

        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 112104`
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

    def test_list_order_with_admin_login(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_order_detail_with_admin_login(self):
        response = self.client.get(reverse('order-list'))
        order = response.data[0]
        response = self.client.get(
            reverse('order-detail', args=[order['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_order_with_name_filter_with_admin_login(self):
        order_query = {'equips_sn': TestData.orders['ME 112104']['equips']}
        response = self.client.get(reverse('order-list'), order_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AdminUpdateOrderTest(APITestCase):
    """
    Update order information with admin privilege
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), equip)

        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 112104`
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        self.order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), self.order)

    def test_update_order_with_admin_login(self):
        order_query = {'equips_sn': self.order['equips']}
        response = self.client.get(reverse('order-list'), order_query)
        order = response.data[0]
        self.order.update({'total_cost': 10000})
        response = self.client.put(
            reverse('order-detail', args=[order['id']]), self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_cost'], self.order['total_cost'])


class UserCreateOrderWithoutLoginTest(APITestCase):
    """
    Create a order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), equip)

        self.client.logout()

    def test_create_order(self):
        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 112104`
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        self.order['tenant'] = TestData.user['mike']['username']
        response = self.client.post(reverse('order-list'), self.order)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteOrderWithoutLoginTest(APITestCase):
    """
    Non-admin user can not delete order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), equip)

        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 112104`
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        response = self.client.post(reverse('order-list'), order)
        self.order = response.data

        self.client.logout()

    def test_delete_order(self):
        response = self.client.delete(
            reverse('order-detail', args=[self.order['id']]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListOrderWithoutLoginTest(APITestCase):
    """
    Non-admin user can list order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), equip)

        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 112104`
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        response = self.client.post(reverse('order-list'), order)
        self.order = response.data

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

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112104'])
        self.client.post(reverse('equip-list'), equip)

        self.client.logout()

        # Create a non-admin user Mike and then login again
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.client.login(**mike)

    def test_create_order(self):
        order = copy.deepcopy(TestData.orders['ME 112104'])
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

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112104'])
        self.client.post(reverse('equip-list'), equip)

        self.client.logout()

        # Create a non-admin user Mike and then login again
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.client.login(**mike)

        order = copy.deepcopy(TestData.orders['ME 112104'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

    def test_delete_order(self):
        response = self.client.get(reverse('order-list'))
        order = response.data[0]
        response = self.client.delete(
            reverse('order-detail', args=[order['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserListOrderTest(APITestCase):
    """
    Non-admin user can list order.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associated to Haulotte
        star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112104'])
        self.client.post(reverse('equip-list'), equip)

        # Create an equipment `ME 112108` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112108'])
        self.client.post(reverse('equip-list'), equip)

        self.client.logout()

        # Create a non-admin user Mike and then login again
        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)
        self.client.login(**mike)

        # Create an equipment `ME 112108` associated to manufacture `Haulotte`
        # and model `star 10`
        equip = copy.deepcopy(TestData.equip['ME 112108'])
        self.client.post(reverse('equip-list'), equip)

        # Create an order to associated to tenant `Mike` and the
        # equipment `ME 111501`
        order = copy.deepcopy(TestData.orders['ME 112104-112108'])
        # Must set the tenant of the order
        order['tenant'] = TestData.user['mike']['username']
        self.client.post(reverse('order-list'), order)

    def test_list_order(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_order_detail(self):
        response = self.client.get(reverse('order-list'))
        order = response.data[0]
        response = self.client.get(
            reverse('order-detail', args=[order['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_order_with_name_filter(self):
        order_query = {'equips_sn': TestData.orders['ME 112104-112108']['equips']}
        response = self.client.get(reverse('order-list'), order_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
