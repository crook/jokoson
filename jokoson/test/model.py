import copy
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from jokoson.test.data import TestData


class AdminCreateModelTest(APITestCase):
    """
    Create a model with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

    def test_create_model_with_admin_login(self):
        td_star_10 = TestData.model['star-10']
        response = self.client.post(reverse('model-list'), td_star_10)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_model_with_invalid_manufacture(self):
        td_star_10 = TestData.model['star-10']
        invalid_model = copy.deepcopy(td_star_10)
        invalid_model['manufacture'] ='Not-Exist'
        response = self.client.post(reverse('model-list'), invalid_model)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AdminDeleteModelTest(APITestCase):
    """
    Delete a model with the admin privilege.
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

    def test_delete_model_with_admin_login(self):
        response = self.client.get(reverse('model-list'))
        model = response.data[0]
        response = self.client.delete(
            reverse('model-detail', args=[model['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListModelTest(APITestCase):
    """
    List a model and model detail with the admin privilege.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

    def test_list_model_with_admin_login(self):
        response = self.client.get(reverse('model-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_model_detail_with_admin_login(self):
        response = self.client.get(reverse('model-list'))
        model = response.data[0]
        response = self.client.get(
            reverse('model-detail', args=[model['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_model_with_name_filter_with_admin_login(self):
        model_query = {'name': TestData.model['star-10']['name']}
        response = self.client.get(reverse('model-list'), model_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AdminUpdateModelTest(APITestCase):
    """
    Update model information with admin privilege
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture  `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        self.star_10 = copy.deepcopy(TestData.model['star-10'])
        self.client.post(reverse('model-list'), self.star_10)

    def test_update_model_with_admin_login(self):
        model_query = {'name': self.star_10['name']}
        response = self.client.get(reverse('model-list'), model_query)
        model = response.data[0]
        self.star_10.update({'name': 'Changed'})
        response = self.client.put(
            reverse('model-detail', args=[model['id']]), self.star_10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.star_10['name'])


class UserCreateModelTest(APITestCase):
    """
    Create a model.
    """
    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create manufacture: Haulotte
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        self.client.logout()

    def test_create_model(self):
        # Create a model `star 10` associate to Haulotte
        td_star_10 = TestData.model['star-10']
        response = self.client.post(reverse('model-list'), td_star_10)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteModelTest(APITestCase):
    """
    Non-admin user can not delete model.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create manufacture: Haulotte
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        self.client.logout()

    def test_delete_model(self):
        response = self.client.get(reverse('model-list'))
        model = response.data[0]
        response = self.client.delete(
            reverse('model-detail', args=[model['id']]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListModelTest(APITestCase):
    """
    Non-admin user can list model.
    """

    def setUp(self):
        td_john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        # Create a manufacture `Haulotte`
        td_Haulotte = TestData.manufacture['Haulotte']
        self.client.post(reverse('manufacture-list'), td_Haulotte)

        # Create a model `star 10` associate to Haulotte
        star_10 = TestData.model['star-10']
        self.client.post(reverse('model-list'), star_10)

        self.client.logout()

    def test_list_model_with_admin_login(self):
        response = self.client.get(reverse('model-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_model_detail_with_admin_login(self):
        response = self.client.get(reverse('model-list'))
        model = response.data[0]
        response = self.client.get(
            reverse('model-detail', args=[model['id']]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_model_with_name_filter_with_admin_login(self):
        model_query = {'name': TestData.model['star-10']['name']}
        response = self.client.get(reverse('model-list'), model_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
