from .models import Data_Type_Collection as cdb
from django.core.exceptions import PermissionDenied


def user_has_permissions(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        database = cdb.objects.get(pk = kwargs['pk'])
        if user in database.authorized_contributors.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
