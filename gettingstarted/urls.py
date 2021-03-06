from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as account_views
from hello import views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^databases/(?P<pk>\d+)/$', views.SubmissionListView.as_view(),
            name = 'comp_tables'),
    url(r'^databases/(?P<pk>\d+)/new$',views.create_submission,
            name = 'create_submission'),
    url(r'^db', views.db, name='db'),
    url(r'^signup/$', account_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    url(r'^upload/$', views.simple_upload, name='upload'),
    url(r'^upload/(?P<pk>\d+)/successful$', views.upload_success, name='upload_success'),
    url(r'^about/', views.about, name='about'),
    url(r'^settings/account/$', account_views.UserUpdateView.as_view(), name = 'account_settings'),
    url(r'^signup/request_successful/', account_views.signup_success, name = 'signup_success'),
    url(r'^database_request/',views.new_database_request,name = "new_db"),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
