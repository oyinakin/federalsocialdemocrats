from django.urls import path, include

from . import views
from django.views import generic
app_name = 'accounts'
urlpatterns = [

path('signin', views.signin, name='signin'),
path('dashboard', views.dashboard, name='dashboard'),
]
