from django import forms
from django.forms import ModelForm,HiddenInput, TextInput, DateInput, NumberInput, Select
from .models import Members
from functools import partial
from datetime import datetime


GENDER = (('Female', 'Female'),('Male', 'Male'))
MARITAL_STATUS = (('Divorced', 'Divorced'),('Married', 'Married'), ('Separated', 'Separated'),('Single', 'Single'),('Widowed', 'Widowed'))
QUALIFICATION =(('PhD','PhD'),('Masters','Masters'),('Bachelors, HND or Equivalent','Bachelors, HND or Equivalent'),
('OND, NCE or Equivalent','OND, NCE or Equivalent'),('SSCE','SSCE'),('Primary School','Primary School'),
('Never attended school','Never attended school'))
OCCUPATION =(('Artisan/Farmer/Hand-Work','Artisan/Farmer/Hand-Work'),('Civil Servant','Civil Servant'),('Employed (Private Sector/NGO)','Employed (Private Sector/NGO)'),
('Entrepreneur/Business Owner','Entrepreneur/Business Owner'),('Unemployed','Unemployed'),('Retired','Retired'),
('Never attended school','Never attended school'))

class MemberForm(ModelForm):
    class Meta:
        model = Members
        exclude = ['UserID']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'middle_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control '}),
            'gender': Select(attrs={'class': 'form-control'}, choices =GENDER),
            'email': TextInput(attrs={'class': 'form-control'}),
            'phone_number': NumberInput(attrs={'class': 'form-control'}),
            'date_of_birth': DateInput(format='%d/%m/%Y',attrs={"type": 'date','class': 'form-control'}),
            'marital_status': Select(attrs={"type": 'date','class': 'form-control'}, choices =MARITAL_STATUS),
            'country_of_residence': Select(attrs={'class': 'form-control','onchange':'getState(this.value)'}),
            'state_of_origin': Select(attrs={'class': 'form-control','onchange':'getLGA(this.value)'}),
            'LGA': Select(attrs={'class': "form-control"}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'state_of_residence': Select(attrs={'class': 'form-control','onchange':'getLGAResidence(this.value)'}),
            'LGA_of_residence': Select(attrs={'class': "form-control"}),
            'whatsapp_number': TextInput(attrs={'class': 'form-control'}),
            'highest_academic_qualification': Select(attrs={'class': 'form-control'},choices=QUALIFICATION),
            'current_occupation':Select(attrs={'class': 'form-control'},choices=OCCUPATION),
            'date_of_registration':TextInput(attrs={'type':'hidden','class': 'form-control','value':datetime.now().strftime("%Y-%m-%d")}),
            }

class HitListForm(forms.Form):
        first_name_1= forms.CharField(label='First Name', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name_1 = forms.CharField(label='Last Name', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
        email_1 = forms.CharField(label='Email', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
class LoginForm(forms.Form):
        email = forms.CharField(label='Email', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
        password = forms.CharField(label='Password', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','type':'password'}))
        confirmpassword = forms.CharField(label='Password', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','type':'password'}))
