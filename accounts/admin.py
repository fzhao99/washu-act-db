from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

def activate_users(modeladmin, request, queryset):
    queryset.update(is_active = True)
activate_users.short_description = "Activate User"


def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active = False)
deactivate_users.short_description = "Deactivate User"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','first_name', 'last_name', 'is_active','is_staff']
    ordering = ['username','is_active','email','first_name', 'last_name','is_staff' ]
    actions = [deactivate_users,activate_users]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
