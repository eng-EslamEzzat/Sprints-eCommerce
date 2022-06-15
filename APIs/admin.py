from django.contrib import admin
from .models import ProductState, User, Brand, Category, Image, Product, Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Image)
admin.site.register(ProductState)
admin.site.register(User)