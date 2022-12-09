from django.db import models
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug=models.CharField(max_length=200)
    body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=('-pub_date',)
    
    def __str__(self):
        return self.title

class NewTable(models.Model):
    bigint_f=models.BigIntegerField()
    bool_f=models.BooleanField()
    date_f=models.DateField(auto_now=True)
    char_f=models.CharField(max_length=20,unique=True)
    datetime_f=models.DateTimeField(auto_now_add=True)
    decimal_f=models.DecimalField(max_digits=10,decimal_places=2)
    float_f=models.FloatField(null=True)
    int_f=models.IntegerField(default=2010)
    text_f=models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=20,unique=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    qty=models.DecimalField(max_digits=5,decimal_places=2,default=0)

    def __str__(self):
        return self.name
