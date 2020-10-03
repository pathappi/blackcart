from django.db import models
from django.conf import settings

# Create your models here.
class Store(models.Model):
    store_id = models.CharField(max_length=300, db_index=True)
    name = models.CharField(max_length=300, blank=False, null=False)
    PLATFORM_CHOICES = (
        settings.PLATFORMS['WOOCOMMERCE'],
        settings.PLATFORMS['SHOPIFY'],
    )
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES, null=False, blank=False)

    store_url = models.CharField(max_length=300, blank=False, null=False)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # to enforce platform id uniqueness
    class Meta:
        unique_together = ('store_id', 'platform')