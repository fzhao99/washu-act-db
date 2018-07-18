from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from .views import *

from .models import Data_Type_Collection as cdb
from .models import Active_Group, Submissions

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)

class HomeTests(TestCase):
    def setUp(self):
        self.cdb = cdb.objects.create(name = 'AMS Database2', description = 'Aerodyne AMS',
                num_tables= 2, admins = 'admin')
        url = reverse('index')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

    def test_home_view_contains_link_to_page(self):
        database_url = reverse('comp_tables', kwargs = {'pk':self.cdb.pk})
        self.assertContains(self.response, 'href="{0}"'.format(database_url))

class DatabaseTests(TestCase):
    def setUp(self):
        cdb.objects.create(name='AMS Database2',description = 'Aerodyne AMS',
                num_tables = 2, admins='admin')
    #check if status code returns 200 (found) for given creation
    def test_database_topics_view_success_status_code(self):
        url = reverse('comp_tables', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    #check if status code returns 404 ( not found) for given bad creation
    def test_database_topics_view_not_found_status_code(self):
        url = reverse('comp_tables', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    #check if status code is using the correct funtion by matching back tot he urlpatterns
    #and checking to make sure the function called was correct
    def test_database_topics_url_resolves_database_topics_view(self):
        view = resolve('/databases/1/')
        self.assertEquals(view.func, comp_tables)

    def test_db_topics_view_contains_navigation_links(self):
        table_url = reverse('comp_tables', kwargs={'pk': 1})
        home_url = reverse('index')
        new_submission_url = reverse('create_submission', kwargs={'pk': 1})

        response = self.client.get(table_url)
        self.assertContains(response,'href="{0}"'.format(home_url))
        self.assertContains(response,'href="{0}"'.format(new_submission_url))


class NewGroupsTest(TestCase):
    def setUp(self):
        cdb.objects.create(name='AMS Database2',description = 'Aerodyne AMS',
                num_tables = 2, admins='admin')
        User.objects.create_user(username='john', email='john@doe.com', password='123')

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
        url = reverse('create_submission', kwargs={'pk':99})
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
