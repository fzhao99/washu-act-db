from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.views.generic import UpdateView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.mail import mail_admins
from django.conf import settings
from hello.models import Data_Type_Collection as cdb

from pathlib import Path


from .forms import SignUpForm

# Create your views here.
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'myaccount.html'
    success_url = reverse_lazy('account_settings')

    def get_object(self):
        return self.request.user

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            public_users = Group.objects.get(name="Public Users")
            user = form.save()
            user.groups.add(public_users)
            # will call redirect to signup success using signal
            databases = cdb.objects.all()
            for database in databases:
                if database.public:
                    database.authorized_contributors.add(user)
            email_admins()
            return render(request,'signup_success.html')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def email_admins():
    email_file = open(str(Path(__file__).parents[1])
            + r'\templates\user_created_email.txt', 'r+')
    email = email_file.read()
    email_file.close()
    subject_file = open(str(Path(__file__).parents[1])
            + r'\templates\user_created_email_subject.txt','r')
    subject = subject_file.read()
    email_file.close()
    subject = subject.strip('\n')
    mail_admins(subject,email)

@receiver(pre_save, sender = User)
def signup_success( sender, instance, **kwargs):
    if instance._state.adding and (not instance.is_superuser):
        instance.is_active = False

    else:
        pass
