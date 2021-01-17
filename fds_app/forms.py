from django import forms
from django.forms import ModelForm,HiddenInput, TextInput, DateInput, NumberInput, Select
from .models import Members,Post,Category
from functools import partial
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import validate_email
from ckeditor.fields import RichTextField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

GENDER = (('Female', 'Female'),('Male', 'Male'))
MARITAL_STATUS = (('Divorced', 'Divorced'),('Married', 'Married'), ('Separated', 'Separated'),('Single', 'Single'),('Widowed', 'Widowed'))
QUALIFICATION =(('PhD','PhD'),('Masters','Masters'),('Bachelors, HND or Equivalent','Bachelors, HND or Equivalent'),
('OND, NCE or Equivalent','OND, NCE or Equivalent'),('SSCE','SSCE'),('Primary School','Primary School'),
('Never attended school','Never attended school'))
OCCUPATION =(('Artisan/Farmer/Hand-Work','Artisan/Farmer/Hand-Work'),('Civil Servant','Civil Servant'),('Employed (Private Sector/NGO)','Employed (Private Sector/NGO)'),
('Entrepreneur/Business Owner','Entrepreneur/Business Owner'),('Unemployed','Unemployed'),('Retired','Retired'),
('Never attended school','Never attended school'))
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class MemberForm(ModelForm):
    class Meta:
        model = Members
        exclude = ['UserID']
        fields = ['first_name','middle_name','last_name','gender','email','phone_number','date_of_birth','marital_status',
        'country_of_residence','state_of_origin','LGA','state_of_residence','LGA_of_residence','whatsapp_number',
        'highest_academic_qualification','current_occupation','date_of_registration'
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'middle_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control '}),
            'gender': Select(attrs={'class': 'form-control'}, choices =GENDER),
            'email': TextInput(attrs={'class': 'form-control'}),
            'phone_number': NumberInput(attrs={'class': 'form-control',"id":"telephone",'type':'tel'}),
            'date_of_birth': DateInput(format='%d/%m/%Y',attrs={"type": 'date','class': 'form-control'}),
            'marital_status': Select(attrs={"type": 'date','class': 'form-control'}, choices =MARITAL_STATUS),
            'country_of_residence': Select(attrs={'class': 'form-control','onchange':'getState(this.value)'}),
            'state_of_origin': Select(attrs={'class': 'form-control','onchange':'getLGA(this.value)'}),
            'LGA': Select(attrs={'class': "form-control"}),
            # 'phone_number': TextInput(attrs={'class': 'form-control'}),
            'state_of_residence': Select(attrs={'class': 'form-control','onchange':'getLGAResidence(this.value)'}),
            'LGA_of_residence': Select(attrs={'class': "form-control"}),
            'whatsapp_number': NumberInput(attrs={'class': 'form-control',"id":"wtelephone",'type':'tel'}),
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
class sendSMSForm(forms.Form):
        sendto = forms.CharField(label='Send To',widget=forms.Textarea(attrs={'class': 'form-control','cols':100,'rows':1}))
        text_message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control','cols':100,'rows':6}))

class sendEmailForm(forms.Form):
      recipient = forms.CharField(label='Send To',widget=forms.Textarea(attrs={'class': 'form-control','cols':100,'rows':1}))
      subject = forms.CharField(label='Message', widget=forms.TextInput(attrs={'class': 'form-control','style':'width:88%'}))
      mail_message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control','cols':100,'rows':6}))

class PostForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.ModelChoiceField(queryset =User.objects.filter(is_staff=True),
                                    empty_label='--Select--',
                                    widget=forms.Select(attrs={'class': 'form-control'}),label='Author',
                                    )
    #updated_on = forms.DateTimeField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Title', widget=CKEditorUploadingWidget())
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),label='Status',
    choices=STATUS)
    summary =forms.CharField(label='Summary', widget=forms.Textarea(attrs={'class': 'form-control','cols':100,'rows':1}))
    #post_images = forms.ImageField(label='Featured Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    category=forms.ModelChoiceField(queryset =Category.objects.all(),
                                    empty_label='--Select--',
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    label='Category',
                                    )
class EditPostForm(forms.Form):
    edittitle = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    editauthor = forms.ModelChoiceField(queryset =User.objects.filter(is_staff=True),
                                    empty_label='--Select--',
                                    widget=forms.Select(attrs={'class': 'form-control'}),label='Author',
                                    )
    #updated_on = forms.DateTimeField(label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    editcontent = forms.CharField(label='Title', widget=CKEditorUploadingWidget())
    editstatus = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),label='Status',
    choices=STATUS)
    editsummary =forms.CharField(label='Summary', widget=forms.Textarea(attrs={'class': 'form-control','cols':100,'rows':1}))
    #post_images = forms.ImageField(label='Featured Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    editcategory=forms.ModelChoiceField(queryset =Category.objects.all(),
                                    empty_label='--Select--',
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    label='Category',
                                    )
