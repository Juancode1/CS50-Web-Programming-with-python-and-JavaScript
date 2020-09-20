from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class listing(models.Model):
    Cats=[
        ('Fa','Fashion'),
        ('To','Toys'),
        ('El','Electronics'),
        ('Ho','Home'),
        ('Cl','clothes'),
    ]
    title=models.CharField(max_length=64)
    description=models.TextField()
    currentprice=models.IntegerField()
    photo=models.ImageField(upload_to='biduploads/%Y/%m/%d/',blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")
    category=models.CharField(choices=Cats,max_length=64) 
    def __str__(self):
        return  f"{self.title}"

class bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bider")
    product=models.ForeignKey(listing,on_delete=models.CASCADE,related_name="bid")
    bid=models.IntegerField()

class comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    product=models.ForeignKey(listing,on_delete=models.CASCADE,related_name="comment")
    comment=models.TextField()