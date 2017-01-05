from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.test.data import TestData


class CSVUploadTests(APITestCase):
    def upload_file(self, path):
        f = open(path, 'rb')
        return {'datafile': f}

    def setUp(self):
        td_john = TestData.user['john']
        User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

    def test_upload_file(self):
        data = self.upload_file('/home/stack/jokoson/jokoson/csv/summary.csv')
        self.client.post(reverse('csv-list'), data, format='multipart')

        response = self.client.get(reverse('manufacture-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse('model-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(reverse('equip-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class CSVDownloadTest(APITestCase):
    def upload_file(self, path):
        f = open(path, 'rb')
        return {'datafile': f}

    def setUp(self):
        td_john = TestData.user['john']
        User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        data = self.upload_file('/home/stack/jokoson/jokoson/csv/summary.csv')
        self.client.post(reverse('csv-list'), data, format='multipart')

    def test_download_file(self):
        self.client.get(reverse('csv-list'))
