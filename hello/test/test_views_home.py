from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from ..views import *

from ..models import Data_Type_Collection as cdb
from ..models import Active_Group, Submissions

import os


class HomeTests(TestCase):
    def setUp(self):
        self.cdb = cdb.objects.create(name = 'AMS Database2', description = 'Aerodyne AMS',
                num_tables= 2, admins = 'admin')
        url = reverse('index')
        self.client = Client()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

    def test_home_view_contains_link_to_page(self):
        database_url = reverse('comp_tables', kwargs = {'pk':self.cdb.pk})
        self.assertContains(self.response, 'href="{0}"'.format(database_url))
