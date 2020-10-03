from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('product.urls')),
    path('store/', include('stores.urls')),
]
