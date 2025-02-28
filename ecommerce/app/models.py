from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
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
    stock=models.IntegerField()
    catg=models.ForeignKey(Category,on_delete=models.CASCADE)
    mcatg=models.ForeignKey(Main_cat,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Plants=models.ForeignKey(Plants,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.FloatField()
    
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn=models.IntegerField()
    pin=models.IntegerField()
    loc=models.TextField()
    adrs=models.TextField()
    city=models.TextField()
    state=models.TextField()

class Bookings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pro=models.ForeignKey(Plants,on_delete=models.CASCADE)
    qty=models.TextField()
    price=models.FloatField()
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(_("Payment Status"), default=PaymentStatus.PENDING,max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_('Signature ID'),max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"