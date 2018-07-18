import requests, os
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings


from .models import Data_Type_Collection as cdb
from .models import Active_Group, Submissions
from .forms import NewGroupForm
from .models import Greeting


# Create your views here.
def index(request):
    databases = cdb.objects.all()
    return render(request, 'home.html',{'databases':databases})

def comp_tables(request, pk):
    database = get_object_or_404(cdb,pk=pk)
    return render(request,'table.html',{'database':database})

def file_upload(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES['test_file'])
    path = default_storage.save(save_path, request.FILES['test_file'])
    return default_storage.path(path)

def create_submission(request, pk):
    database = get_object_or_404(cdb, pk=pk)
    user = User.objects.first()  #TODO make user auth
    if request.method == 'POST':
        form = NewGroupForm(request.POST,request.FILES)
        if form.is_valid():
            # file_upload(request=request)
            group = form.save(commit=False)
            group.database = database
            group.name=form.cleaned_data.get('name')
            group.authorized_contributors = user
            group.save()

            submission = Submissions.objects.create(
                link_of_data = request.FILES['link_of_data'].name,
                link_of_metadata = request.FILES['link_of_metadata'].name,
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
