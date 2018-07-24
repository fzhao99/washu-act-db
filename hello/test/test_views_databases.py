from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from ..views import *

from ..models import Data_Type_Collection as cdb
from ..models import Active_Group, Submissions

import os


class DatabaseTests(TestCase):
    def setUp(self):
        cdb.objects.create(name='AMS Database2',description = 'Aerodyne AMS',
                num_tables = 2, admins='admin')
        self.client = Client()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
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
