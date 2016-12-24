from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.db import serializers
from jokoson.db import models
from jokoson import exception
from rest_framework.exceptions import ValidationError


class AdminCreateCategoryTest(APITestCase):
    """
    Create a category with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            'name': 'star-10',
            'description': 'This is a star-10!',
        }

    def test_create_category_with_admin_login(self):
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminDeleteCategoryTest(APITestCase):
    """
    Delete a category with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        self.data = {
            'name': 'star-10',
            'description': 'This is a star-10!',
        }
        self.client.post(reverse('category-list'), self.data)

    def test_delete_category_with_admin_login(self):
        category = models.Category.objects.get(name='star-10')
        response = self.client.delete(
            reverse('category-detail', args=[category.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminListCategoryTest(APITestCase):
    """
    List a category and category detail with the admin privilege.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

        category = {
            'name': 'star-10',
            'description': 'This is a star-10!',
        }
        self.category = models.Category.objects.create(**category)

    def test_list_category_with_admin_login(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_get_category_detail_with_admin_login(self):
        response = self.client.get(
            reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_list_category_with_name_filter_with_admin_login(self):
        category_name = 'star-10'
        category = {'name': category_name}
        response = self.client.get(reverse('category-list'), category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], category_name)


class AdminUpdateCategoryTest(APITestCase):
    """
    Update category information with admin privilege
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.category = models.Category.objects.create(
            name="star-10", description="This is a star-10")
        self.data = serializers.CategorySerializer(self.category).data
        self.data.update(
            {'name': 'star-8', 'description': "This is a star-8"}, )

    def test_update_category_with_admin_login(self):
        response = self.client.put(
            reverse('category-detail', args=[self.category.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.data['name'])
        self.assertEqual(response.data['description'], self.data['description'])


class UserCreateCategoryTest(APITestCase):
    """
    Create a category.
    """

    def setUp(self):
        self.data = {
            'name': 'star-10',
            'description': 'This is a star-10',
        }

    def test_create_category(self):
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class UserDeleteCategoryTest(APITestCase):
    """
    Non-admin user can not delete category.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            'name': 'star-10',
            'description': 'This is a star-10!',
        }
        self.client.post(reverse('category-list'), self.data)
        self.client.logout()

    def test_delete_category(self):
        category = models.Category.objects.get(name='star-10')
        with self.assertRaises(exception.NoPermissionToDeleteCategory):
            self.client.delete(reverse('category-detail', args=[category.id]))


class UserListCategoryTest(APITestCase):
    """
    Non-admin user can list category.
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        category = {
            'name': 'star-10',
            'description': 'This is a star-10!',
        }
        self.category = models.Category.objects.create(**category)
        self.client.logout()

    def test_list_category(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_get_category_detail(self):
        response = self.client.get(
            reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_list_category_with_name_filter(self):
        category_name = 'star-10'
        category = {'name': category_name}
        response = self.client.get(reverse('category-list'), category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], category_name)