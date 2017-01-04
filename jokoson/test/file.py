from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jokoson.test.data import TestData


class FileUploadTests(APITestCase):
    def upload_file(self, path):
        f = open(path, 'rb')
        return {'datafile': f}

    def test_upload_file(self):
        td_john = TestData.user['john']
        User.objects.create_superuser(**td_john)
        self.client.login(**td_john)

        mike = TestData.user['mike']
        self.client.post(reverse('user-list'), mike)

        data = self.upload_file('/home/stack/jokoson/jokoson/csv/summary.csv')

        self.client.post(reverse('csv-list'), data, format='multipart')

        response = self.client.get(reverse('manufacture-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('model-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
