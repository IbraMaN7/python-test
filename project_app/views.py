from django.http import JsonResponse
from django.views.generic import ListView

from .models import Supply

import json

def up_base(datasheets, price_ru):
    """
    :param datasheets:
    :type list(list):
    :param price_ru:
    :type float:
    """
    for item in datasheets:
        if Supply.objects.filter(order_id=item[1]):
            suppply_current = Supply.objects.get(order_id=item[1])
            suppply_current.price_usd=float(item[2])
            suppply_current.price_ru=round(float(item[2])*price_ru, 5)
            suppply_current.date_supply='{2}-{1}-{0}'.format(*str(item[3]).split('.'))
            suppply_current.save()
        else:    
            suppply_current = Supply(
                                order_id=item[1],
                                price_usd=item[2],
                                price_ru=round(float(item[2])*price_ru, 5),
                                date_supply='{2}-{1}-{0}'.format(*str(item[3]).split('.')))
            suppply_current.save()
            item.append(round(int(item[2])*price_ru, 5))

def supply_lists(request):
    data = [{'id':i.id, 
             'order_id':i.order_id, 
             'price_usd':i.price_usd, 
             'price_ru':i.price_ru, 
             'date_supply':i.date_supply}
                for i in Supply.objects.filter()]

    return JsonResponse({'data':data})    

class DashbroadView(ListView):
    model = Supply
    template_name = 'dashbroad.html'