from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from .forms import MemberForm, HitListForm, LoginForm
from .models import Members, Post, HitList
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def index(request):
    template = loader.get_template('fds_app/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def wherewestand(request):
    template = loader.get_template('fds_app/wherewestand.html')
    context = {}
    return HttpResponse(template.render(context, request))

def whoweare(request):
    template = loader.get_template('fds_app/whoweare.html')
    context = {}
    return HttpResponse(template.render(context, request))

def takeaction(request):
    template = loader.get_template('fds_app/takeaction.html')
    context = {}
    return HttpResponse(template.render(context, request))

def joiningpolitics(request):
    template = loader.get_template('fds_app/joiningpolitics.html')
    context = {}
    return HttpResponse(template.render(context, request))

def elections2023(request):
    template = loader.get_template('fds_app/2023elections.html')
    context = {}
    return HttpResponse(template.render(context, request))

def news(request):
    template = loader.get_template('fds_app/news.html')
    context = {"posts":Post.objects.all()}
    return HttpResponse(template.render(context, request))
def post_detail(request, slug):
    template = loader.get_template('fds_app/post_detail.html')
    post = Post.objects.filter(slug=slug)
    return render(request, 'fds_app/post_detail.html', {'post': post[0]})

def signup(request):
    template = loader.get_template('fds_app/signup.html')
    context = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # member = Members(date_of_registration =datetime.now().strftime("%d/%m/%Y"))
        #
        form = MemberForm(request.POST)
        form.fields['date_of_registration'].initial =datetime.now().strftime("%Y-%m-%d")
        # check whether it's valid:
        if form.is_valid():
            if Members.objects.filter(email=request.POST['email']).count()>0:
                print('email exists')
                return render(request, 'fds_app/signup.html', {'form': form,
                         'error_message': "The email has already been registered",
                         })
            else:
               request.session['refdata'] = request.POST
               User.objects.create_user(
                 request.POST['email'],
                 request.POST['email'], request.POST['password'],
                 first_name = request.POST['first_name'],
                 last_name = request.POST['last_name'])
               form.save()
               # process the data in form.cleaned_data as required
               # ...
               #redirect to a new URL:
               sendcode = send_mail(
               "Your registration was successful",
               'Dear '+  request.POST['first_name'] +' ' +  request.POST['first_name'],
               from_email="Federal Social Democrats<"+settings.EMAIL_HOST_USER+">",
               recipient_list=  request.POST['email'],
               fail_silently=False,
               )
               return HttpResponseRedirect('thankyou')
        else:
            print(form.errors)
            return render(request, 'fds_app/signup.html',{'form':form,'form2':LoginForm(),'error_message':form.errors })
    # if a GET (or any other method) we'll create a blank form
    else:
        form = MemberForm()
        form2 = LoginForm()
        return render(request, 'fds_app/signup.html', {'form': form,'form2':form2})

def referral(request):
    template = loader.get_template('fds_app/referral.html')
    context = {}
    refdata = request.session['user']
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # member = Members(date_of_registration =datetime.now().strftime("%d/%m/%Y"))
        form = HitListForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
           entry = HitList.objects.filter(email=form.cleaned_data['email_1']).count()
           if entry>0:
             freq = entry.high_frequency
             print("No of hits: " + str(entry.high_frequency))
             if freq==1:
                 print("freq is 1")
                 entry.update(high_frequency = 2,
                   ref2_email=refdata['email'],
                   ref2_date= datetime.now().strftime("%Y-%m-%d"), )

             if freq ==2:
                 print("freq is 2 Send email")
                 entry.update(high_frequency = 3,
                   ref3_email=refdata['email'],
                   ref3_date= datetime.now().strftime("%Y-%m-%d"), )
             if freq ==3:
                 print("freq is 3 No email")


           else:
             print("No hits in database: " )
             HitList.objects.create(
               ref1_email=refdata['email'],
               ref1_date= datetime.now().strftime("%Y-%m-%d"),
               first_name=form.cleaned_data['first_name_1'],
               last_name=form.cleaned_data['last_name_1'],
               email = form.cleaned_data['email_1'],
               high_frequency = 1)
           # process the data in form.cleaned_data as required
           # ...
           # redirect to a new URL:
           return HttpResponseRedirect(reverse('fds_app:referral'))
        else:
            print(form.errors)
            return render(request, 'fds_app/referral.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = HitListForm()
        return render(request, 'fds_app/referral.html', {'form': form})

def thankyou(request):
    template = loader.get_template('fds_app/thankyou.html')
    context = {}
    return HttpResponse(template.render(context, request))

def dashboard(request):
    template = loader.get_template('admin/index.html')
    context = {}
    labels = ['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    data = [0,0,0,0,0,0,0,0,0,0,0,0]
    month_summary = (Members.objects
              .annotate(month=Month('date_of_registration'))
              .values('month')
              .annotate(total=Count('id'))
              .order_by('month'))
    for i in month_summary:
        if  calendar.month_abbr[month_summary[i]['month']] in  labels:
            data[i] =  month_summary[i]['total']

    return render(request, 'admin/index.html', {'labels': labels,'data':data})
