from django.urls import path, include

from django.contrib.auth import views as auth_views
from . import views
from django.views import generic
app_name = 'accounts'
urlpatterns = [
path('signin', views.signin, name='signin'),
path('dashboard', views.dashboard, name='dashboard'),
path('signout', views.signout, name='signout'),
path('verify_transaction', views.verify_transaction, name='verify_transaction'),
path('signin', views.signin, name='signin'),
# path('password_reset',views.password_reset,name='password_reset',),
# path('password_reset/done',views.password_reset_done,name='password_reset_done',),
# path('reset/<uidb64>/<token>/',views.password_reset_confirm,name='password_reset_confirm',),
# path('reset/done/',views.password_reset_complete,name='password_reset_complete',),

]
