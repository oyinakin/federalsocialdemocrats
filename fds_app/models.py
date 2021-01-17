from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

from django.core.validators import validate_email
GENDER = (('Female', 'Female'),('Male', 'Male'))
MARITAL_STATUS = (('Divorced', 'Divorced'),('Married', 'Married'), ('Separated', 'Separated'),('Single', 'Single'),('Widowed', 'Widowed'))
QUALIFICATION =(('PhD','PhD'),('Masters','Masters'),('Bachelors, HND or Equivalent','Bachelors, HND or Equivalent'),
('OND, NCE or Equivalent','OND, NCE or Equivalent'),('SSCE','SSCE'),('Primary School','Primary School'),
('Never attended school','Never attended school'))

OCCUPATION =(('Artisan/Farmer/Hand-Work','Artisan/Farmer/Hand-Work'),('Civil Servant','Civil Servant'),('Employed (Private Sector/NGO)','Employed (Private Sector/NGO)'),
('Entrepreneur/Business Owner','Entrepreneur/Business Owner'),('Unemployed','Unemployed'),('Retired','Retired'),
('Never attended school','Never attended school'))
TRANSTYPE = (('Subscription', 'Subscription'),('Donation', 'Donation'))
PAYMENT_METHOD = (('Card', 'Card'),('Bank', 'Bank'),('USSD', 'USSD'),('Transfer', 'Transfer'))

class NewsAuthor(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)

    def __str__(self):
        return self.first_name +' '+ self.last_name

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    news_id = models.CharField(max_length=5)
    news_title = models.TextField()
    news_short_description = models.CharField(max_length=300)
    news_full_content = models.TextField()
    news_published_on = models.DateField()
    news_author = models.ForeignKey(NewsAuthor, on_delete=models.CASCADE)

    def __str__(self):
        return self.news_title
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True,blank = True,)
    content = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    summary = models.TextField()
    category=models.ForeignKey(Category, on_delete= models.CASCADE)
    image_url=models.CharField(max_length=200, blank=True)
    image_extension=models.CharField(max_length=200, blank=True)
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
class PostComment(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post, on_delete= models.CASCADE)

class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
class PostTag(models.Model):
    post=models.ForeignKey(Post, on_delete= models.CASCADE)
    tag=models.ForeignKey(Tag, on_delete= models.CASCADE)



class Transactions(models.Model):
    transaction_reference = models.CharField(max_length=70)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=70)
    middle_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    amount = models.FloatField(max_length=70)
    payment_type =  models.CharField(max_length=12, choices=TRANSTYPE)
    payment_channel = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    date_of_transaction = models.DateTimeField()


class HitList(models.Model):
    email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    ref1_email = models.EmailField(max_length=70)
    ref1_date = models.DateField()
    ref2_email = models.EmailField(max_length=70, blank = True, null= True)
    ref2_date = models.DateField(blank = True, null= True)
    ref3_email = models.EmailField(max_length=70, blank = True, null= True)
    ref3_date = models.DateField(blank = True, null= True)
    high_frequency = models.IntegerField(default = 0)

class Members(models.Model):
    UserID = models.CharField(max_length=7)
    first_name = models.CharField(max_length=70)
    middle_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=200,validators=[validate_email])
    gender = models.CharField(max_length=7, choices=GENDER)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS)
    country_of_residence = models.CharField(max_length=70)
    state_of_origin =  models.CharField(max_length=70)
    LGA = models.CharField(max_length=70)
    state_of_residence =  models.CharField(max_length=70)
    LGA_of_residence = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=16)
    whatsapp_number = models.CharField(max_length=16)
    highest_academic_qualification = models.CharField(max_length=29, choices=QUALIFICATION)
    current_occupation = models.CharField(max_length=29, choices=OCCUPATION)
    date_of_registration = models.DateField(default = datetime.now().strftime("%Y-%m-%d"))
    def clean_dor(self):
        if not self['date_of_registration'].html_name in self.data:
            return self.fields['date_of_registration'].initial
        return self.cleaned_data['date_of_registration']
