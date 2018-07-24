import requests, os
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .models import Data_Type_Collection as cdb
from .models import Active_Group, Submissions
from .forms import NewGroupForm
from .models import Greeting


# Create your views here.

@login_required
def index(request):
    databases = cdb.objects.all()
    return render(request, 'home.html',{'databases':databases})

@login_required
def comp_tables(request, pk):
    database = get_object_or_404(cdb,pk=pk)
    return render(request,'table.html',{'database':database})

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
def create_submission(request, pk):
    database = get_object_or_404(cdb, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = NewGroupForm(request.POST,request.FILES)
        if form.is_valid():
            # file_upload(request=request)
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

            submission = Submissions.objects.create(
                link_of_data = data_uploaded_file_url,
                link_of_metadata = metadata_uploaded_file_url,
                data_name =  request.FILES['link_of_data'].name,
                metadata_name = request.FILES['link_of_metadata'].name,
                created_by = user,
                group = group,
                database = database
            )
            return redirect('comp_tables', pk=database.pk)  # TODO: redirect to the created topic page
    else:
        form = NewGroupForm()
    return render(request,'submission.html',{'database':database, 'form':form})


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
