from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from ..views import *

from ..models import Data_Type_Collection as cdb
from ..models import Active_Group, Submissions
from django.core import mail

import os


class NewGroupsTest(TestCase):
    def setUp(self):
        cdb.objects.create(name='AMS Database2',description = 'Aerodyne AMS',
                num_tables = 2, admins='admin')
        self.client = Client()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
    def test_create_submission_url_resolves_create_submission_view(self):

        view = resolve('/databases/1/new')
        self.assertEqual(view.func, create_submission)

    def test_create_submission_view_success_status_code(self):
        url = reverse('create_submission', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_create_submission_view_not_found_status_code(self):
        url = reverse('create_submission', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_csrf(self):
        url = reverse('create_submission', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_create_submission_valid_post_data(self):
        url = reverse('create_submission', kwargs={'pk': 1})
        data_test_file = open('hello/testfiles/test.txt')
        data_test_contents = data_test_file.read()
        data_test_file.close()
        metadata_test_file = open('hello/testfiles/metadata.txt')
        metadata_test_contents = metadata_test_file.read()
        metadata_test_file.close()

        file_data = {
            'name':'Test Group',
            'link_of_data': SimpleUploadedFile("hello/testfiles/test.txt",
                    bytes(data_test_contents,'utf-8')),
            'link_of_metadata': SimpleUploadedFile("hello/testfiles/metadata.txt",
                    bytes(metadata_test_contents,'utf-8'))
        }
        response = self.client.post(url, file_data)
        self.assertTrue(Active_Group.objects.exists())
        self.assertTrue(Submissions.objects.exists())

    def test_create_submission_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('create_submission', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_create_submission_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('create_submission', kwargs={'pk': 1})
        data = {
            'groupname':'',
            'link_of_data':'',
            'link_of_metadata':''
                }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Active_Group.objects.exists())
        self.assertFalse(Submissions.objects.exists())

    def test_contains_form(self):
        url = reverse('create_submission', kwargs={'pk':1})
        response = self.client.post(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewGroupForm)

    def test_new_submission_invalid_post_data(self):
        '''
        Invalid submission data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('create_submission', kwargs={'pk':1})
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_submission_email_send(self):
        url = reverse('upload_success',kwargs = {'pk':1})
        response = self.client.get(url)
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].subject,"[Django] New Submission")
        self.assertEqual(mail.outbox[0].body,"A new submission has been uploaded. "
                        "Please visit the admin pannel to process the request.")


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        cdb.objects.create(name='Database', description='test database', num_tables=3,
                admins = 'admin')
        self.client.login(username = 'admin', password = 'Numanonpuellaest!1')
        self.url = reverse('create_submission', kwargs={'pk': 1})
        self.response = self.client.get(self.url)


    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
