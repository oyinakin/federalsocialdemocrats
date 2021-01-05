from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = 'fds_app.admin.MyAdminSite'

class FdsAppConfig(AppConfig):
    name = 'fds_app'
