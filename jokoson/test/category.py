from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from jokoson.db import serializers
from jokoson.db import models
from jokoson.test.data import TestData


class AdminCreateCategoryTest(APITestCase):
    """
    Create a category with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)
        self.star_10 = TestData.category['star-10']

    def test_create_category_with_admin_login(self):
        response = self.client.post(reverse('category-list'), self.star_10)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteCategoryTest(APITestCase):
    """
    Delete a category with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        self.star_10 = TestData.category['star-10']
        self.client.post(reverse('category-list'), self.star_10)

    def test_delete_category_with_admin_login(self):
        category = models.Category.objects.get(name=self.star_10['name'])
        response = self.client.delete(
            reverse('category-detail', args=[category.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListCategoryTest(APITestCase):
    """
    List a category and category detail with the admin privilege.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        self.star_10 = TestData.category['star-10']
        self.category = models.Category.objects.create(**self.star_10)

    def test_list_category_with_admin_login(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for key in self.star_10:
            self.assertEqual(response.data[0][key], self.star_10[key])

    def test_get_category_detail_with_admin_login(self):
        response = self.client.get(
            reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in self.star_10:
            self.assertEqual(response.data[key], self.star_10[key])

    def test_list_category_with_name_filter_with_admin_login(self):
        category = {'name': self.star_10['name']}
        response = self.client.get(reverse('category-list'), category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for key in self.star_10:
            self.assertEqual(response.data[0][key], self.star_10[key])


class AdminUpdateCategoryTest(APITestCase):
    """
    Update category information with admin privilege
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        start_8 = TestData.category['star-8']
        star_10 = TestData.category['star-10']
        self.star_10 = serializers.CategorySerializer(
            models.Category.objects.create(**star_10)).data

    def test_update_category_with_admin_login(self):
        start_8 = TestData.category['star-8']
        response = self.client.put(
            reverse('category-detail', args=[self.star_10['id']]), start_8)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in start_8:
            self.assertEqual(response.data[key], start_8[key])


class UserCreateCategoryTest(APITestCase):
    """
    Create a category.
    """

    def test_create_category(self):
        star_10 = TestData.category['star-10']
        response = self.client.post(reverse('category-list'), star_10)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeleteCategoryTest(APITestCase):
    """
    Non-admin user can not delete category.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        star_10 = TestData.category['star-10']
        self.client.post(reverse('category-list'), star_10)

        self.client.logout()

    def test_delete_category(self):
        name = TestData.category['star-10']['name']
        star_10 = models.Category.objects.get(name=name)
        response = self.client.delete(reverse('category-detail',
                                              args=[star_10.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListCategoryTest(APITestCase):
    """
    Non-admin user can list category.
    """

    def setUp(self):
        john = TestData.user['john']
        self.superuser = User.objects.create_superuser(**john)
        self.client.login(**john)

        star_10 = TestData.category['star-10']
        self.star_10 = models.Category.objects.create(**star_10)

        self.client.logout()

    def test_list_category(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        star_10 = TestData.category['star-10']
        for key in star_10:
            self.assertEqual(response.data[0][key], star_10[key])

    def test_get_category_detail(self):
        response = self.client.get(
            reverse('category-detail', args=[self.star_10.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.star_10.name)

    def test_list_category_with_name_filter(self):
        name = TestData.category['star-10']['name']
        category = {'name':name}
        response = self.client.get(reverse('category-list'), category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], name)