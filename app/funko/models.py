from django.db import models

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length=50)


class Pop(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_number = models.IntegerField()
    name = models.CharField(max_length=100)
