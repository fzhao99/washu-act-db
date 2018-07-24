from django.contrib import admin
from .models import Submissions
from .models import Data_Type_Collection as cdb
# Register your models here.


def change_submission_accept(modeladmin, request, queryset):
    queryset.update(status = 'a')
change_submission_accept.short_description = "Accept submission and publish"

def change_submission_deny(modeladmin, request, queryset):
    queryset.update(status = 'd')
change_submission_deny.short_description = "Deny submission outright"

def change_submission_modify(modeladmin, request, queryset):
    queryset.update(status = 'm')
change_submission_modify.short_description = "Deny submission and request modification"

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['group','link_of_data', 'link_of_metadata','status']
    ordering = ['group','link_of_data','link_of_metadata']
    actions = [change_submission_accept,change_submission_deny,change_submission_modify]


admin.site.register(cdb)
admin.site.register(Submissions, SubmissionAdmin)
