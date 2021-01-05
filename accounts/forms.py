from django import forms
from django.forms import ModelForm,HiddenInput, TextInput, DateInput, NumberInput, Select

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

class HitListForm(forms.Form):
        first_name_1= forms.CharField(label='First Name', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name_1 = forms.CharField(label='Last Name', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
        email_1 = forms.CharField(label='Email', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
class LoginForm(forms.Form):
        email = forms.CharField(label='Email', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
        password = forms.CharField(label='Password', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','type':'password'}))
