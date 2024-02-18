from django.db import models
from cloudinary.uploader import upload
from django.utils import timezone

# Create your models here.

def upload_path(instance, filename):
    # make a name as timestam
    return f'products/{instance.name + str(timezone.now())}/{filename}';

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    description = models.CharField(max_length=500, blank=True, verbose_name="Product Description")
    image = models.CharField(max_length=500, verbose_name="Product Image", null=True)
    price = models.FloatField(verbose_name="Product Price")
    company = models.ForeignKey('account.Company', on_delete=models.CASCADE, verbose_name="Company", related_name="products")
    weight = models.CharField(max_length=500,verbose_name="Weight", null=True)
    length = models.CharField(max_length=500,verbose_name="Length", null=True)
    breadth = models.CharField(max_length=500,verbose_name="Breadth", null=True)
    height = models.CharField(max_length=500,verbose_name="Height", null=True)
    units = models.CharField(max_length=10, blank=True, null=True)
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Products", related_name="categories", blank=True, null=True)
        
    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(max_length=500, blank=True, verbose_name="Category Description")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name