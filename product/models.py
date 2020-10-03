from django.db import models
from django.conf import settings

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=300, db_index=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    # decided to add only 1 currency field which will be the product default currency
    # we can use a 3rd partie API to convert the product price in other currencies if needed
    # Unless the logic here is to sale the product for different prices per country, this detail is not specified in the requirements
    # so I decided to go for a proper design
    CURRENCY_CHOICES = (
        settings.CURRENCY['CAD'],
        settings.CURRENCY['EUR'],
        settings.CURRENCY['USD'],
    )
    currency = models.CharField(
        max_length=2, choices=CURRENCY_CHOICES, default=settings.CURRENCY['CAD'])
    stock = models.IntegerField(default=0)
    # variation should actually be a FK so we can have the possibility to add multiple variations as products are different
    # for the purpose of time I will stick to the 'bad' design of adding size and colour on the product table
    PRODUCT_SIZE_CHOICES = (
        settings.PRODUCT_SIZES['UNKNOWN'],
        settings.PRODUCT_SIZES['XS'],
        settings.PRODUCT_SIZES['S'],
        settings.PRODUCT_SIZES['M'],
        settings.PRODUCT_SIZES['L'],
        settings.PRODUCT_SIZES['XL'],
        settings.PRODUCT_SIZES['XXL'],
    )
    size = models.CharField(max_length=2, choices=PRODUCT_SIZE_CHOICES,
                            default=settings.PRODUCT_SIZES['UNKNOWN'])

    # I will use a charfield for color as color could have lot of iterations
    colour = models.CharField(max_length=300, blank=True, default='')

    # we should consider the measurement unit used but ill just leave it like this
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, default='')

    # we need to store the external id to not duplicate an existing product but update it when pulling products
    external_id = models.IntegerField(null=True, blank=False)

    # created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # Foreign Keys
    store = models.ForeignKey('stores.Store', related_name='product_store',
                              on_delete=models.CASCADE, blank=False, null=False, default=1)
