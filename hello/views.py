import requests, os
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView, ListView, View
from django.db.models import Count
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import mail_admins
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


from .models import Data_Type_Collection as cdb
from .models import Active_Group, Submissions
from .forms import NewGroupForm, NewDatabaseRequestForm
from .models import Greeting
from .decorators import user_has_permissions
# Create your views here.


@method_decorator(user_has_permissions, name = 'dispatch')
class SubmissionListView(ListView):
    model = Submissions
    context_object_name = 'submissions'
    template_name = 'table.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['database'] = self.database
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.database = get_object_or_404(cdb, pk = self.kwargs.get('pk'))
        queryset = self.database.submissions.order_by('-updated_at').annotate(replies = Count('link_of_data') - 1)
        return queryset

@login_required
def new_database_request(request):
    if request.method == "POST":
        form = NewDatabaseRequestForm(request.POST)
        if form.is_valid():
            new_database = form.save()
            mail_admins("New Submission","A new submission has been uploaded. "
                        "Please visit the admin pannel to process the request.")
            return render(request, 'request_success.html')

    else:
        form = NewDatabaseRequestForm()
    return render(request, 'new_db_request.html', {'form':form})

def upload_success(request,pk):
    database = get_object_or_404(cdb,pk=pk)
            # email admins of a new submission
    mail_admins("New Submission","A new submission has been uploaded. "
                "Please visit the admin pannel to process the request.")

    return render(request, 'upload_success.html',{'database':database}) # TODO actully check if upload was successful

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

@login_required
def index(request):
    databases = cdb.objects.all()
    current_user = request.user
    return render(request, 'home.html',{'databases':databases,'current_user':current_user})

def about(request):
    return render(request,'about.html')

@login_required
@user_has_permissions
def create_submission(request, pk):
    database = get_object_or_404(cdb, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = NewGroupForm(request.POST,request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.database = database
            group.name=form.cleaned_data.get('name')
            group.authorized_contributors = user
            group.save()

            data_file = request.FILES['link_of_data']
            metadata_file = request.FILES['link_of_metadata']
            fs = FileSystemStorage()
            data_filename = fs.save(data_file.name,data_file)
            metadata_filename = fs.save(metadata_file.name,metadata_file)

            data_uploaded_file_url = fs.url(data_filename)
            metadata_uploaded_file_url = fs.url(metadata_filename)
            try:
                comment_file = request.FILES['comment_file']
                comment_filename = fs.save(comment_file.name,comment_file)
                comment_uploaded_file_url = fs.url(comment_filename)
            except MultiValueDictKeyError:
                comment_uploaded_file_url = None
                pass
            admins = database.admins.all()
            if user in admins:
                accept_status = 'a'
            else:
                accept_status = 's'
            submission = Submissions.objects.create(
                link_of_data = data_uploaded_file_url,
                link_of_metadata = metadata_uploaded_file_url,
                comment_file = comment_uploaded_file_url,
                data_name =  request.FILES['link_of_data'].name,
                metadata_name = request.FILES['link_of_metadata'].name,
                created_by = user,
                group = group,
                database = database,
                status = accept_status
            )

            return redirect('upload_success', pk=database.pk)
    else:
        form = NewGroupForm()
    return render(request,'submission.html',{'database':database, 'form':form})


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
