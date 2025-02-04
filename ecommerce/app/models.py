from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Main_cat(models.Model):
    m_name=models.TextField(unique=True)

    def __str__(self):
        return self.m_name
class Category(models.Model):
    c_name=models.TextField()
    m_cat=models.ForeignKey(Main_cat,on_delete=models.CASCADE)

    def __str__(self):
        return self.c_name
class Plants(models.Model):
    p_id=models.TextField()
    name=models.TextField()
    p_catg=models.TextField()
    p_dis=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    img=models.FileField()
    img2=models.FileField()
    catg=models.ForeignKey(Category,on_delete=models.CASCADE)
    mcatg=models.ForeignKey(Main_cat,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Plants=models.ForeignKey(Plants,on_delete=models.CASCADE)
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn=models.IntegerField()
    pin=models.IntegerField()
    loc=models.TextField()
    adrs=models.TextField()
    city=models.TextField()
    state=models.TextField()