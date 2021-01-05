from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
GENDER = (('Female', 'Female'),('Male', 'Male'))
MARITAL_STATUS = (('Divorced', 'Divorced'),('Married', 'Married'), ('Separated', 'Separated'),('Single', 'Single'),('Widowed', 'Widowed'))
QUALIFICATION =(('PhD','PhD'),('Masters','Masters'),('Bachelors, HND or Equivalent','Bachelors, HND or Equivalent'),
('OND, NCE or Equivalent','OND, NCE or Equivalent'),('SSCE','SSCE'),('Primary School','Primary School'),
('Never attended school','Never attended school'))

OCCUPATION =(('Artisan/Farmer/Hand-Work','Artisan/Farmer/Hand-Work'),('Civil Servant','Civil Servant'),('Employed (Private Sector/NGO)','Employed (Private Sector/NGO)'),
('Entrepreneur/Business Owner','Entrepreneur/Business Owner'),('Unemployed','Unemployed'),('Retired','Retired'),
('Never attended school','Never attended school'))

class NewsAuthor(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)

    def __str__(self):
        return self.first_name +' '+ self.last_name

class NewsArticle(models.Model):
    news_id = models.CharField(max_length=5)
    news_title = models.TextField()
    news_short_description = models.CharField(max_length=300)
    news_full_content = models.TextField()
    news_published_on = models.DateField()
    news_author = models.ForeignKey(NewsAuthor, on_delete=models.CASCADE)

    def __str__(self):
        return self.news_title

class HitList(models.Model):
    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    ref1_email = models.CharField(max_length=70)
    ref1_date = models.DateField()
    ref2_email = models.CharField(max_length=70, blank = True, null= True)
    ref2_date = models.DateField(blank = True, null= True)
    ref3_email = models.CharField(max_length=70, blank = True, null= True)
    ref3_date = models.DateField(blank = True, null= True)
    high_frequency = models.IntegerField(default = 0)

class Members(models.Model):
    UserID = models.CharField(max_length=7)
    first_name = models.CharField(max_length=70)
    middle_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=7, choices=GENDER)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    country_of_residence = models.CharField(max_length=70)
    state_of_origin =  models.CharField(max_length=70)
    LGA = models.CharField(max_length=70)
    state_of_residence =  models.CharField(max_length=70)
    LGA_of_residence = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=13)
    whatsapp_number = models.CharField(max_length=13)
    highest_academic_qualification = models.CharField(max_length=29, choices=QUALIFICATION)
    current_occupation = models.CharField(max_length=29, choices=OCCUPATION)
    date_of_registration = models.DateField(default = datetime.now().strftime("%Y-%m-%d"))
    def clean_dor(self):
        if not self['date_of_registration'].html_name in self.data:
            return self.fields['date_of_registration'].initial
        return self.cleaned_data['date_of_registration']
