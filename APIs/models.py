from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

class Brand(models.Model):
    name = models.CharField(max_length=250, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=250)
    discription = models.CharField(max_length=500)
    productDetails = models.TextField()
    price= models.DecimalField(max_digits=9, decimal_places=2)
    buyers = models.ManyToManyField(User, related_name='purchases', blank=True)
    categories = models.ManyToManyField(Category, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_exists = models.BooleanField(default=True)
    availability = models.IntegerField(default=0)
    attributes = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ('-created_at',)

    @property
    def avg_rating(self):
        return self.reviews.aggregate(avg_rating = models.Avg('rating'))["avg_rating"]

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to = "images/", blank=True, null=True)


class Review(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField(default=0, validators = [
            MaxValueValidator(5),
            MinValueValidator(0),
        ])
    comment = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'product',)


class Order(models.Model):

    ORDER_STATUSES = (
        ('pending','PENDING'),
        ('in review','IN_REVIEW'),
        ('canceled','CANCELLED'),
        ('in progress','IN_PROGRESS'),
        ('on the way','ON_THE_way'),
        ('delivered', 'DELIVERED'),
    )
    
    buyer = models.ForeignKey(User, on_delete= models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='oreders')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUSES,
                                         default=ORDER_STATUSES[0][0])
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)