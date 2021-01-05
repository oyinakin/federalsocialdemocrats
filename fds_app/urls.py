from django.urls import path, include

from . import views
from django.views import generic
app_name = 'fds_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('wherewestand', views.wherewestand, name='wherewestand'),
    path('whoweare', views.whoweare, name='whoweare'),
    path('takeaction', views.takeaction, name='takeaction'),
    path('2023elections', views.elections2023, name='2023elections'),
    path('joiningpolitics', views.joiningpolitics, name='joiningpolitics'),
    path('signup', views.signup, name='signup'),
    path('referral', views.referral, name='referral'),
    path('thankyou', views.thankyou, name='thankyou'),

]
