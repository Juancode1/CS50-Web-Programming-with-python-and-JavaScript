from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
    pass

class listing(models.Model):
    Cats=[
        ('Fashion','Fashion'),
        ('Toys','Toys'),
        ('Electronics','Electronics'),
        ('Home','Home'),
        ('Clothes','Clothes'),
        ('Food','Food'),
        ('Shoes','Shoes'),
        ('Other','Other')
    ]
    title=models.CharField(max_length=64,verbose_name="Item ")
    description=models.TextField(verbose_name="Description ")
    currentprice=models.IntegerField(verbose_name="Price ")
    photo=models.ImageField(upload_to='biduploads/%Y/%m/%d/',blank=False,verbose_name="Picture of item ")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="seller")
    category=models.CharField(choices=Cats,default=('Other','Other'),max_length=64,verbose_name="Category ")
    publishdate=models.DateField(auto_now_add=True) 
    terminated=models.BooleanField(auto_created=False)
    def __str__(self):
        return  f"{self.title}"

class bids(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="bider")
    product=models.ForeignKey(listing,on_delete=models.CASCADE,related_name="product")
    bid=models.IntegerField()

class comments(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="commenter")
    product=models.ForeignKey(listing,on_delete=models.CASCADE,related_name="comment")
    comment=models.TextField()

class sold(models.Model):
    product=models.OneToOneField(listing,on_delete=models.CASCADE)
    seller=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="fseller")
    buyer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="fbuyer")
    price=models.IntegerField()
    solddate=models.DateTimeField(auto_now_add=True)
    