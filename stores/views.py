from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .models import Store
from product.models import Product
from api.tasks.product_importer import *

def get_products(request, store_id):
    HttpResponse(store_id)
    function_mapper = {
        settings.PLATFORMS['WOOCOMMERCE'][0]: WoocommerceImporter(),
        settings.PLATFORMS['SHOPIFY'][0]: ShopifyImporter(),
    }
    if store_id is None:
        raise('No Store id passed')
    else:
        try:
            store = Store.objects.get(store_id=store_id)
        except Store.DoesNotExist:
            raise('Store id {} Invalid').format(store_id)
        function_mapper[store.platform].run(store)
    return HttpResponse('Request Ran')

def hello_world(request, store_id):
    text = 'Hello World ' + str(store_id)
    return HttpResponse(text)

        
