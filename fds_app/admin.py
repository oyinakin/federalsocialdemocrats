from django.contrib import admin
from .models import Members, HitList
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case,Count, When
from django.db.models.functions import TruncMonth
from django.db.models import Func
from django.db import models
import calendar
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from .forms import MemberForm, HitListForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class MyAdminSite(AdminSite):

     @never_cache
     def index(self, request, extra_context=None):
         template = loader.get_template('admin/index.html')
         labels = ['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
         data = [0,0,0,0,0,0,0,0,0,0,0,0]
         month_summary = (Members.objects
                   .annotate(month=Month('date_of_registration'))
                   .values('month')
                   .annotate(total=Count('id'))
                   .order_by('month'))
         top5new =  Members.objects.order_by('-date_of_registration')[:5]
         allmembers = Members.objects.all()
         hitlist = HitList.objects.all()

         for i in range(len(month_summary)):
            if  calendar.month_abbr[month_summary[i]['month']] in  labels:
                 data[i] =  month_summary[i]['total']
         if extra_context is None:
            extra_context = {}
         extra_context =  {"labels":labels,"data":data,"top5new":top5new,
          "allmemberscount":allmembers.count(),
          "allmemberslist":allmembers,
          "hitlistcount":hitlist.count(),
          "hitlist":hitlist,
         }
         return super(MyAdminSite, self).index(request, extra_context)

     @never_cache
     def logout(self, request, extra_context=None):
            template = loader.get_template('admin/logout.html')
            context = {}
            return super(MyAdminSite, self).logout(request, extra_context)

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Members)
admin_site.register(HitList)

# Register your models here.
