from django.conf import settings
from product.models import Product
from requests import HTTPError
from datetime import datetime
from woocommerce import API

import requests
import logging


logger = logging.getLogger('django')

class BaseProductsImporter():
    def __init__(self):
        super().__init__()
        self.header = {
            "Content-Type": "application/json",
        }
    
    def run(self, store):
        external_products = self.get_external_products(store)
        self.import_external_products(external_products)

    def get_external_products(self, store):
        pass

    def import_external_products(self, external_products):
        pass


class WoocommerceImporter(BaseProductsImporter): 
    def __init__(self):
        super().__init__()

    def get_client(self, store_url):
        self.api_settings = settings.PLATFORMS_API_SETTINGS['WOOCOMMERCE']
        client = API(
            url=store_url,
            consumer_key=self.api_settings['consumer_key'],
            consumer_secret=self.api_settings['consumer_secret'],
            wp_api=self.api_settings['wp_api'],
            version=self.api_settings['version'],
        )
        return client

    def get_external_products(self, store):
        client = self.get_client(store.store_url)
        response = client.get("products").json()
        if response.status_code == 200:
            return response
        else:
            raise(response)

    def import_external_products(self, products_list):
        # we should normally create a map for the fields matching. Not enough time to implement all of those
        for product in products_list:
            existing_product = Product.objects.filter(
                external_id=product['id'])
            if existing_product.count() > 0:
                existing_product.update(name=product['name'], price=int(
                    product['price']), stock=product['stock_quantity'])
            else:
                Product.objects.create(external_id=product['id'], name=product['name'], price=int(
                    product['price']), stock=product['stock_quantity'])


class ShopifyImporter(BaseProductsImporter):
    def __init__(self):
        super().__init__()
        
    # not a good practice but ok for the little test
    # we should normally have a shoppify having all the different requests supported
    def make_product_request_url(self, store_id):
        self.api_settings = settings.PLATFORMS_API_SETTINGS['SHOPIFY']
        request_url = 'https://' + self.api_settings['apikey'] + ':' + self.api_settings['password'] + \
            '@' + store_id + \
            '.myshopify.com/admin/products.json'
        return request_url

    def get_external_products(self, store):
        request_url = self.make_product_request_url(store.store_id)
        r = requests.get(request_url)
        if r.status_code == 200:
            return r.json()['products']
        else:
            raise(r)

    def import_external_products(self, products_list):
        # we should normally create a map for the fields matching. Not enough time to implement all of those
        # shopify handles variations as additional products, a good practice will be to loop through variations as well
        for product in products_list:
            existing_product = Product.objects.filter(
                external_id=product['id'])
            if existing_product.count() > 0:
                existing_product.update(name=product['title'], price=int(
                    product['price']), stock=product['inventory_quantity'])
            else:
                Product.objects.create(external_id=product['id'], name=product['title'], price=int(
                    product['price']), stock=product['inventory_quantity'])
