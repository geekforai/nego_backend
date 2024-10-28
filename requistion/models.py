from django.db import models
from django.contrib.auth.models import User

class Requisition(models.Model):
    class Status(models.TextChoices):
        CREATED = 'Created', 'Created'
        FULFILLED = 'Fulfilled', 'Fulfilled'
    
    class Currency(models.TextChoices):
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
     

    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    delivery_date = models.DateField()
    negotiation_closure_date = models.DateField()
    type_of_currency = models.CharField(max_length=3, choices=Currency.choices)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_terms = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
   

