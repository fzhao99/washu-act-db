import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'gettingstarted.settings')
django.setup()

from django.contrib.auth.models import User
from hello.models import *



db = Data_Type_Collection.objects.get(name = "AMS Database")
user = User.objects.first()


for i in range(100):
    datafile = open("data.txt", "w+")
    metafile = open("meta.txt", "w+")

    name = "Test Group " + str(i)
    group = Active_Group.objects.create(name = name, authorized_contributors = user, database = db)
    submission = Submissions.objects.create(database = db, data_name = "test", metadata_name = "test meta", group = group, created_by=user,
            status = 'a')

    datafile.close()
    metafile.close()
