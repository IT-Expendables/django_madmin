from django.conf import settings
from django.urls import path
from . import views


if settings.DEBUG:
    from django.utils.autoreload import file_changed
    file_changed.disconnect(dispatch_uid='template_loaders_file_changed')


madmin_urls = [
    path('madmin/upload/', views.upload, name="upload"),
    path('madmin/check_upload/', views.check_upload, name="check_upload"),
]
