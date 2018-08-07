from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import os
# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

def get_all_users():
    return User.objects.all()
def get_admin():
    superusers = []
    for user in User.objects.all():
        if user.is_superuser:
            superusers.append(user)
    return superusers
    


class Data_Type_Collection(models.Model):
    name = models.CharField(max_length=30, unique = True)
    description = models.CharField(max_length=100)
    last_post = models.DateTimeField(null=True)
    admins = models.ManyToManyField(User, default = get_admin, related_name = "db_admins")
    authorized_contributors = models.ManyToManyField(User, default = get_all_users,
            related_name = "auth_contributors")
    def __str__(self):
        return self.name

    def get_accepted_posts_count(self):
        filter_subs = Submissions.objects.filter(group__database=self)
        accepted_subs = 0
        for sub in filter_subs:
            if sub.status == 'a':
                accepted_subs += 1
        return accepted_subs

    def get_first_accepted_post(self):
        filter_subs = Submissions.objects.filter(group__database=self)
        ordered_subs= filter_subs.order_by('status','-created_at')
        first_post = ordered_subs.first()
        return first_post

class Active_Group(models.Model):
    name = models.CharField(max_length=30)
    authorized_contributors= models.ForeignKey(User, related_name='auth_members',
            on_delete = models.CASCADE,)
    database = models.ForeignKey('Data_Type_Collection', related_name='groups',
            on_delete = models.CASCADE,)

    def __str__(self):
        return self.name
STATUS_CHOICES=(
    ('s', 'Submitted for Approval'),
    ('a', 'Accepted'),
    ('d', 'Denied'),
    ('m', 'Subject to Modification')
)

class Submissions(models.Model):
    link_of_data = models.FileField(upload_to='testfiles/')
    link_of_metadata = models.FileField(upload_to='testfiles/')
    comment_file = models.FileField(upload_to='testfiles/')
    data_name = models.CharField(max_length=100)
    metadata_name = models.CharField(max_length=100)
    database = models.ForeignKey('Data_Type_Collection', related_name='submissions',
            on_delete = models.CASCADE,)
    group = models.ForeignKey('Active_Group',related_name='submissions',
            on_delete = models.CASCADE,)
    created_by = models.ForeignKey(User, related_name='submissions',
            on_delete = models.CASCADE,)
    updated_by = models.ForeignKey(User, null=True, related_name='+',
            on_delete = models.CASCADE,)
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)
    status = models.CharField(max_length=1, choices = STATUS_CHOICES, default='s')


    def __str__(self):
        return os.path.basename(self.link_of_data.name)
