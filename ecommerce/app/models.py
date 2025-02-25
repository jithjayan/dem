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

class Buy(models.Model):

    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Plants,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    qnty=models.PositiveBigIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default="Pending")# New field for tracking delivery status

    def __str__(self):
        return f"{self.product.name} ({self.status})"
    

class Order(models.Model):
    buy = models.OneToOneField(Buy, on_delete=models.SET_NULL, null=True, blank=True)  # # Link Order to Buy
    customer_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Allows null values
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)  # Allows null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name} on {self.created_at}"