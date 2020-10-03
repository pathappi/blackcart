from django.urls import path
from .views import get_products, hello_world

urlpatterns = [
    path('<int:store_id>/', hello_world),
    path('<int:store_id>/products/', get_products),
]