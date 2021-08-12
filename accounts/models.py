from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    phone = PhoneNumberField(null=True,blank=True,max_length=30)
    email = models.EmailField(max_length=200,null=True,blank=True,unique=True)
    profile_pic = models.ImageField(null=True,blank=True,upload_to='images/')
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    
    def __str__(self):
        return self.name if self.name else ''
class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    CATEGORIES = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor')
    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CATEGORIES)
    description = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.name
class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
