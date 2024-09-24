from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid


ORDER_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('success', 'Success'),
    ('cancel', 'Cancel'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    content = models.TextField(default=None)
    image = models.ImageField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.CharField(max_length=350,null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,null=True)
    bookauthor = models.ForeignKey(Author, on_delete=models.CASCADE,null=True)
    price = models.FloatField(default=None)
    qty = models.IntegerField(default=None)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=None)

        
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=8, editable=False)
    product = models.JSONField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=None)
    total_qty = models.IntegerField(default=None)
    name = models.CharField(max_length=30, default=None)
    phone = models.IntegerField(default=None)
    address = models.TextField(default=None)
    status = models.CharField(max_length=20,choices=ORDER_CHOICES,default='pending')
    created_at = models.DateTimeField(default=None)
    
    def __str__(self):
        return str(self.id)
      
      
class mostsell(models.Model):
    image = models.ImageField(default=None)
    created_at = models.DateTimeField(default=datetime.now)

class Feedback(models.Model):
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    message = models.TextField(default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    image = models.ImageField(default=None,null=True)
    dob = models.DateField(default=None,null=True)
    address = models.CharField(max_length=300,default=None,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __int__(self):
        return self.user.username
