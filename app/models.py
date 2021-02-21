from django.db import models

# Create your models here.

class Donation(models.Model):
    name=models.CharField(max_length=300)
    amount=models.CharField(max_length=1000)
    email=models.EmailField( max_length=254)
    order_id = models.CharField(max_length=1000 )
    payment_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False)
