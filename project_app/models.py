from django.db import models

# Create your models here.
class Supply(models.Model):
    order_id = models.IntegerField()
    price_usd = models.DecimalField(max_digits=15, decimal_places=5) #models.IntegerField()
    price_ru = models.DecimalField(max_digits=15, decimal_places=5) #models.IntegerField()
    date_supply = models.DateField() #models.DateTimeField()