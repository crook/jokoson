import copy
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
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to `Haulotte`
        td_star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), td_star_10)

    def test_create_equip_with_admin_login(self):
        td_equip = TestData.equip['ME 112104']
        response = self.client.post(reverse('equip-list'), td_equip)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteEquipTest(APITestCase):
    """
    Delete a equip with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to `Haulotte`
        td_star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), td_star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`
        td_equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), td_equip)

    def test_delete_equip_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        equip = response.data[0]
        response = self.client.delete(
            reverse('equip-detail', args=[equip['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListEquipTest(APITestCase):
    """
    List a equip and equip detail with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        td_star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), td_star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`
        td_equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), td_equip)

    def test_list_equip_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_equip_detail_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        equip = response.data[0]
        response = self.client.get(
            reverse('equip-detail', args=[equip['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_equip_with_name_filter_with_admin_login(self):
        equip = {'sn': TestData.equip['ME 112104']['sn']}
        response = self.client.get(reverse('equip-list'), equip)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AdminListAllEquipTest(APITestCase):
    """
    List a equip and equip detail with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        td_star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), td_star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`
        td_equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), td_equip)

        td_equip = TestData.equip['ME 111501']
        response = self.client.post(reverse('equip-list'), td_equip)
        print(response)

    def test_list_all_equip_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class AdminUpdateEquipTest(APITestCase):
    """
    Update equip information with admin privilege
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`
        self.equip = copy.deepcopy(TestData.equip['ME 112104'])
        self.client.post(reverse('equip-list'), self.equip)

    def test_update_equip_with_admin_login(self):
        equip_query = {'sn': self.equip['sn']}
        response = self.client.get(reverse('equip-list'), equip_query)
        model = response.data[0]
        self.equip.update({'sn': 'Changed', 'health': 'BAD'})
        response = self.client.put(
            reverse('equip-detail', args=[model['id']]), self.equip)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sn'], self.equip['sn'])


class UserCreateEquipTest(APITestCase):
    """
    Create a equip.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to `Haulotte`
        td_star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), td_star_10)

        self.client.logout()

    def test_create_equip(self):
        td_equip = TestData.equip['ME 112104']
        response = self.client.post(reverse('equip-list'), td_equip)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteEquipTest(APITestCase):
    """
    Non-admin user can not delete equip.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to `Haulotte`
        td_star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), td_star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`
        td_equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), td_equip)

        self.client.logout()

    def test_delete_equip(self):
        response = self.client.get(reverse('equip-list'))
        equip = response.data[0]
        response = self.client.delete(
            reverse('equip-detail', args=[equip['id']]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListEquipTest(APITestCase):
    """
    Non-admin user can list equip.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        td_star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), td_star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`
        td_equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), td_equip)

        self.client.logout()

    def test_list_equip_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_equip_detail_with_admin_login(self):
        response = self.client.get(reverse('equip-list'))
        equip = response.data[0]
        response = self.client.get(
            reverse('equip-detail', args=[equip['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_equip_with_name_filter_with_admin_login(self):
        equip = {'sn': TestData.equip['ME 112104']['sn']}
        response = self.client.get(reverse('equip-list'), equip)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UserListGoodEquipTest(APITestCase):
    """
    Non-admin user can list the equipment which health is `OK`.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        td_star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), td_star_10)

        # Create an equipment `ME 112104` associate to manufacture `Haulotte`
        # and model `star 10`, which health is `OK`
        td_equip = TestData.equip['ME 112104']
        self.client.post(reverse('equip-list'), td_equip)

        # Create an equipment `ME 111501` associate to manufacture `Haulotte`
        # and model `star 10`, which health is `BAD`
        td_equip = TestData.equip['ME 111501']
        self.client.post(reverse('equip-list'), td_equip)

        self.client.logout()

    def test_list_good_equip(self):
        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
