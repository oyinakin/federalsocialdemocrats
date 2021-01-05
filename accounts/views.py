from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from fds_app.forms import MemberForm, HitListForm, LoginForm
from fds_app.models import Members, HitList
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
           login(request, user)
           # Redirect to a success page.
           request.session['user'] = request.POST
           return HttpResponseRedirect('dashboard')
        else:
            form = LoginForm()
            return render(request, 'accounts/signin.html', {'form': form,
                    'error_message': "Invalid username or password",
                    })
            # Return an 'invalid login' error message.
    else:
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form': form})
def dashboard(request):
    template = loader.get_template('accounts/dashboard.html')
    context = {}
    message =""
    refdata = request.session['user']
    print(refdata["email"])
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # member = Members(date_of_registration =datetime.now().strftime("%d/%m/%Y"))
        form = HitListForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
           entry = Members.objects.filter(email=form.cleaned_data['email_1']).count()
           if  entry>0:
                message = "Your contact is already a member of FSD. Thank you for the referral. You can refer someone else."
                return render(request, 'accounts/dashboard.html', {'form': HitListForm(),'message':message})

           entry = HitList.objects.filter(email=form.cleaned_data['email_1'])
           if entry.count()>0:
             freq = entry[0].high_frequency
             print("No of hits: " + str(entry[0].high_frequency))
             if freq==1:
                 print("freq is 1")
                 entry.update(high_frequency = 2,
                   ref2_email=refdata['email'],
                   ref2_date= datetime.now().strftime("%Y-%m-%d"), )
                 message = "Your contact has been invited before, but we have send them another invite"
                 return render(request, 'accounts/dashboard.html', {'form': HitListForm(),'message':message})
             if freq ==2:
                 print("freq is 2 Send email")
                 entry.update(high_frequency = 3,
                   ref3_email=refdata['email'],
                   ref3_date= datetime.now().strftime("%Y-%m-%d"), )
                 message = "Your contact has been invited before, but we have send them  another invite"
                 return render(request, 'accounts/dashboard.html', {'form': HitListForm(),'message':message})
             if freq ==3:
                 print("freq is 3 No email")
                 message = "Your contact has been invited too many times but is yet to register. We don’t want to disturb them anymore. Thank you."
                 return render(request, 'accounts/dashboard.html', {'form': HitListForm(),'message':message})
           else:
             print("No hits in database: " )
             HitList.objects.create(
               ref1_email=refdata['email'],
               ref1_date= datetime.now().strftime("%Y-%m-%d"),
               first_name=form.cleaned_data['first_name_1'],
               last_name=form.cleaned_data['last_name_1'],
               email = form.cleaned_data['email_1'],
               high_frequency = 1)
             message = "Your contact has been sent an email inviting them to join FSD.Thank you."

             return render(request, 'accounts/dashboard.html', {'form': HitListForm(),'message':message})

        else:
            print(form.errors)
            return render(request, 'accounts/dashboard.html')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = HitListForm()
        return render(request, 'accounts/dashboard.html', {'form': form})
    return HttpResponse(template.render(context, request))
