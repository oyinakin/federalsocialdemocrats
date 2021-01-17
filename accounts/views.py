from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, Http404, HttpResponseRedirect
from django.template import loader
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from fds_app.forms import MemberForm, HitListForm, LoginForm
from .forms import paymentForm,ChangePasswordForm
from fds_app.models import Members, HitList, Transactions
from django.contrib.auth.models import User
from django.contrib.auth import views, login, authenticate,logout
from django.contrib.auth.decorators import login_required
import requests
import json
from django.core.mail import send_mail
from django.conf import settings
from decouple import config
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

           return HttpResponseRedirect(reverse('accounts:dashboard'))
        else:
            form = LoginForm()
            return render(request, 'accounts/signin.html', {'form': form,
                    'error_message': "Invalid username or password",
                    })
            # Return an 'invalid login' error message.
    else:
        form = LoginForm()
        return render(request, 'accounts/signin.html', {'form': form})

def password_reset(request):

    return HttpResponseRedirect(reverse('accounts:password_reset_confirm'))

def password_reset_confirm(request):
    pass

def signout(request):
    try:
        del request.session['user']
    except KeyError:
        print("del issue")
        pass
    logout(request)
    return HttpResponseRedirect('signin', {'error_message': "You are signed out"})

def dashboard(request):
    template = loader.get_template('accounts/dashboard.html')
    context = {}
    message =""
    try:
        refdata = request.session['user']
    except:
      return HttpResponseRedirect('signin', {'error_message': "You are not signed in"})

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

        elif paymentForm(request.POST).is_valid():
            payform= paymentForm(request.POST)
            paymessage ="got here"
            print(payform.errors)
            #context = {'active_tab':'transactions',"paymessage":paymessage, 'payform': paymentForm(initial={'amount':0.00})}
            #return render(request, 'accounts/dashboard.html', {'active_tab':'transactions',"paymessage":paymessage, 'payform': paymentForm(initial={'amount':0.00})})

            return HttpResponse("paymessage")
    # if a GET (or any other method) we'll create a blank form
    else:
        form2 = HitListForm()
        user = Members.objects.filter(email=refdata['email'])
        transactionlist= Transactions.objects.filter(email=refdata['email']).order_by('-date_of_transaction')
        data = {'email':refdata['email'],
        "first_name" : user[0].first_name,
        "middle_name" : user[0].middle_name,
        "last_name" : user[0].last_name,
        "amount":0.00}
        payform = paymentForm(data)
        cpwordform = ChangePasswordForm()
        form = MemberForm()
        member = Members.objects.get(email=refdata['email'])
        form = MemberForm(instance=member)
        return render(request, 'accounts/dashboard.html', {'transactionlist':transactionlist,'cpwordform' : cpwordform , 'form2': form2,'form': form, 'payform': payform} )
    return HttpResponse(template.render(context, request))

def verify_transaction(request):
    refdata = request.session['user']
    user = Members.objects.filter(email=refdata['email'])
    data = request.POST
    headers = {"Authorization": "Bearer " + config("PAYSTACK_SECRET_KEY")}
    url = "https://api.paystack.co/transaction/verify/"+data["reference"]
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    results = response.json()
    Transactions.objects.create(
      transaction_reference = data["reference"],
      email = data["email"],
      first_name = data['first_name'],
      middle_name = data['middle_name'],
      last_name =data['last_name'],
      amount = data['amount'],
      payment_type =  data['transtype'],
      payment_channel = results['data']['channel'],
      status = results['data']['status'],
      date_of_transaction = results['data']['paid_at'],
      )
    if results['data']['status'] == 'success':
          status_message = "Your transaction: "+data["reference"] + " was successful."
    elif results['data']['status'] == 'failed':
            status_message = "Your transaction: "+data["reference"] + " failed."
    else:
          status_message = ""
    transactionlist= Transactions.objects.filter(email=refdata['email']).order_by('-date_of_transaction')
    print(transactionlist)
    jsondata = {
        "transactionlist": list(transactionlist.values()),
        'status_message':status_message,
    }
    sendcode = send_mail(
    "Your Payment has been received",
    'Dear '+  request.POST['first_name'] +' ' +  request.POST['first_name'],
    from_email="Federal Social Democrats<"+settings.EMAIL_HOST_USER+">",
    recipient_list=  [request.POST['email']],
    fail_silently=False,
    )
    return JsonResponse(jsondata)
