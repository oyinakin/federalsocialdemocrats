from django.contrib import admin
from django.utils.text import slugify
from django.urls import path, include
from .models import Members, HitList, Transactions,Post,Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case,Count, When
from django.db.models.functions import TruncMonth
from django.db.models import Func
from django.db import models
import calendar, re, os, traceback
from django.core.mail import send_mail
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect,JsonResponse
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from .forms import MemberForm, HitListForm, LoginForm, sendSMSForm,sendEmailForm,PostForm,EditPostForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.conf import settings
import requests, json
class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class MyAdminSite(AdminSite):


     @never_cache
     def index(self, request, extra_context=None):
         site_title =''
         index_title =''
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
         sendsmsform = sendSMSForm()
         sendemailform = sendEmailForm
         transactions = Transactions.objects.all().order_by('-date_of_transaction')
         STATUS = (
             (0,"Draft"),
             (1,"Publish")
         )
         for i in range(len(month_summary)):
            if  calendar.month_abbr[month_summary[i]['month']] in  labels:
                 data[i] =  month_summary[i]['total']
         if extra_context is None:
            extra_context = {}
         extra_context =  {"labels":labels,"data":data,"top5new":top5new,
          "allmemberscount":allmembers.count(),
          "categories":Category.objects.all(),
          "allmemberslist":allmembers,
          "hitlistcount":hitlist.count(),
          "hitlist":hitlist,
          "sendsmsform":sendsmsform,
          "sendemailform":sendemailform,
          "transactions":transactions,
          "transactionstop5":transactions[:5],
          'form':MemberForm(),
          'postform':PostForm(),
          'editpostform':EditPostForm(),
          'news':Post.objects.all(),
          "POSTSTATUS": [ {0:"Draft"},
             {1:"Publish"}
          ]
         }
         return super(MyAdminSite, self).index(request, extra_context)

     @never_cache
     def logout(self, request, extra_context=None):
            template = loader.get_template('admin/logout.html')
            context = {}
            return super(MyAdminSite, self).logout(request, extra_context)

     def sendsms(self, request):

         data = request.POST
         print(data)
         i=0
         for nu in data["sendto"].split(";"):
          if len(nu)>5:
            i=i+1
            print(nu)
            print(data["text_message"])
            print(i)
            payload = {
            "api_token":settings.BULK_SMS_TOKEN_ID,
            "from":"FSDTeam",
            "to":nu.strip(),
            "body":data["text_message"]
            }

            url = "https://www.bulksmsnigeria.com/api/v1/sms/create"

            response = requests.post(url,params=payload)
            response.raise_for_status()
            results = response.json()
         return JsonResponse({'status_message':'Messages sent successfully'})

     def sendemail(self,request):
         data = request.POST
         for nu in data["recipient"].split(";"):
          if len(nu)>5:
            sendcode = send_mail(
            data['subject'],
            data['mail_message'],
            from_email="FSD<"+settings.EMAIL_HOST_USER+">",
            recipient_list= [nu.strip()],
            fail_silently=False,
            )
         return JsonResponse({'status_message':'Messages sent successfully'})
     def applyfilter(self, request):
         data =request.POST
         print(data)
         try:
            key1 = data['state_of_origin[]']
         except KeyError:
            key1 =[]
         try:
             key2 = data['state_of_residence[]']
         except KeyError:
             key2 =[]
         try:
             key3 = data['country_of_residence[]']
         except KeyError:
             key3 =[]
         try:
            key4 = data['gender[]']
         except KeyError:
            key4 =[]
         data2= {
           'gender':key4,
           'state_of_origin':key1,
           'country_of_residence':key3,
           'state_of_residence':key2,
         }
         print(data2)
         filtered_data = Members.objects.all()
         filters =['gender','state_of_origin','state_of_residence','country_of_residence']
         for f in filters:
             if data2[f]:
                 filtered_data = filtered_data.filter(**{f:data2[f]})
         return JsonResponse({'filtered_data':list(filtered_data.values())})

     def getmemberprofile(self, request):
         data = request.POST
         profile = Members.objects.filter(id=data['id'])

         return JsonResponse({'profile':list(profile.values())})
     def editprofile(self,request):
       profile = MemberForm(request.POST)
       print(profile)
       if profile.is_valid():
              user = Members.objects.get(email=request.POST["email"])
              profile = MemberForm(request.POST, instance = user)
              profile.save()
       return JsonResponse({'status_message':'Profile Updated'})

     def postentry(self, request) :
         data = (request.POST)

         form = PostForm(request.POST)
         print(form.errors)
         print(form["content"].value())

         imagelist = re.search('src="([^"]+)',form["content"].value())
         if imagelist:
             imagelistsplit=os.path.splitext(imagelist.group().replace('src="',''))
             image_url =imagelistsplit[0]
             image_extension=imagelistsplit[1]
             print(imageurl)
         else:
             image_url =""
             image_extension=""

         if form.is_valid():
             is_exist=Post.objects.filter(title= form["title"].value(),
             slug=slugify(form["title"].value()))
             if is_exist:
                 return JsonResponse({'status_message':'Entry Title Exists! Go to Post Tabs to edit'})
             slug = slugify(form["title"].value())
             Post.objects.create(
             title = form["title"].value(),
             author = User.objects.filter(id=form["author"].value())[0],
             status = form["status"].value(),
             content = form["content"].value(),
             summary = form["summary"].value(),
             category =Category.objects.filter(id= form["category"].value())[0],
             slug = slug
             )

             return JsonResponse({'status_message':'Entry created successfully'})

         else:
             return JsonResponse({'status_message':'I got here'})
     def getpost(self, request):
        data = request.POST
        post = Post.objects.filter(id=data['id'])
        return JsonResponse({'postprofile':list(post.values())})
     def editpost(self, request):
        data =request.POST
        if data:
            try:
               user= User.objects.get(id=data["author"])
               retrieved_post = Post.objects.get(id=data["id"])
               retrieved_post.slug=slugify(data["title"])
               print(retrieved_post.author)
               print(request.POST["author"])
               status=int(data["status"])
               print(type(status))
               print(data["content"])
               retrieved_post.title = data["title"]
               retrieved_post.status =  data["status"]
               retrieved_post.content = data["content"]
               retrieved_post.summary = request.POST["summary"]
               retrieved_post.category =Category.objects.filter(id= data["category"])[0]
               retrieved_post.author =User.objects.filter(id= data["author"])[0]
               retrieved_post.save()
               return JsonResponse({'status_message':'Post Updated'})
            except:
               print(traceback.format_exc())
               return JsonResponse({'no':'There was an error in updating'})

        else:
            return JsonResponse({'status_message':'There was an error in updating'})

     def changepoststatus(self, request):
         data= request.POST
         try:
           if data["post_status"] == "Publish":
             Post.objects.filter(id__in=request.POST.getlist("postlist[]")).update(status=1)
           if data["post_status"] == "Unpublish":
             Post.objects.filter(id__in=request.POST.getlist("postlist[]")).update(status=0)
           return JsonResponse({'status_message':'Status Updated'})
         except:
             print(traceback.format_exc())
             return JsonResponse({'status_message':'There was an error in updating'})
     def savecategory(self,request):
         data= request.POST
         try:
           is_exist = Category.objects.filter(title=data["category_name"])
           if is_exist:
               return JsonResponse({'error_message':'Category exists already!'})

           else:
               Category.objects.create(
               title = data["category_name"],
               slug = slugify(data["category_name"])
               )
               new_data = Category.objects.all()
               return JsonResponse({'status_message':'Category Added', 'new_data':list(new_data.values())})
         except:
             print(traceback.format_exc())
             return JsonResponse({'error_message':'There was an error in updating'})


     def get_urls(self):
         urls = super().get_urls()
         my_urls = [path('sendsms', self.admin_view(self.sendsms)), path('sendemail', self.admin_view(self.sendemail))
         , path('editprofile', self.admin_view(self.editprofile)),path('applyfilter', self.admin_view(self.applyfilter))
         ,path('postentry', self.admin_view(self.postentry)),path('getpost', self.admin_view(self.getpost)),
         path('editpost', self.admin_view(self.editpost)),path('changepoststatus', self.admin_view(self.changepoststatus)),
         path('getmemberprofile', self.admin_view(self.getmemberprofile)),path('savecategory',self.admin_view(self.savecategory)),
         ]

         return my_urls + urls

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Members)
admin_site.register(HitList)
# Register your models here.
