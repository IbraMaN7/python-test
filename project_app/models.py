from django.db import models


class Supply(models.Model):
    order_id = models.IntegerField(
        verbose_name=u'id продукта')
    price_usd = models.DecimalField(
        max_digits=15, 
        decimal_places=5, 
        verbose_name=u'Стоимость USD')
    price_ru = models.DecimalField(
        max_digits=15, 
        decimal_places=5,
        verbose_name=u'Стоимость РУБ')
    date_supply = models.DateField(
        verbose_name='Дата поставки')

    def __str__(self):
        return str(self.order_id)

    class Meta:
        verbose_name = u'Поставка'
        verbose_name_plural = u'Поставки'
