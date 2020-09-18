from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=999)
    price = models.FloatField()
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    sale_start = models.DateTimeField(blank=True, null=True)
    sale_end = models.DateTimeField(blank=True, null=True)
