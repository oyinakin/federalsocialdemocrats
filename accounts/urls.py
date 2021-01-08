from django.urls import path, include

from . import views
from django.views import generic
app_name = 'accounts'
urlpatterns = [
path('signin', views.signin, name='signin'),
path('dashboard', views.dashboard, name='dashboard'),
path('signout', views.signin, name='signout'),
path('verify_transaction', views.verify_transaction, name='verify_transaction'),
]
