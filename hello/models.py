from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Data_Type_Collection(models.Model):
    name = models.CharField(max_length=30, unique = True)
    description = models.CharField(max_length=100)
    num_tables = models.IntegerField()
    admins = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Active_Group(models.Model):
    name = models.CharField(max_length=30)
    authorized_contributors= models.ForeignKey(User, related_name='auth_user',
            on_delete = models.CASCADE,)
    database = models.ForeignKey('Data_Type_Collection', related_name='groups',
            on_delete = models.CASCADE,)
    def __str__(self):
        return self.name

class Submissions(models.Model):
    link_of_data = models.FileField(upload_to='testfiles/')
    link_of_metadata = models.FileField(upload_to='testfiles/')
    database = models.ForeignKey('Data_Type_Collection', related_name='submissions',
            on_delete = models.CASCADE,)
    group = models.ForeignKey('Active_Group',related_name='submissions',
            on_delete = models.CASCADE,)
    created_by = models.ForeignKey(User, related_name='submissions',
            on_delete = models.CASCADE,)
    updated_by = models.ForeignKey(User, null=True, related_name='+',
            on_delete = models.CASCADE,)

    def __str__(self):
        return self.group_of_submission

    def filename(self):
        return os.path.basename(self.file.name)
