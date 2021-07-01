from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name="add_cart"),
    path('decrease_item/<int:product_id>/<int:cart_item_id>/', views.decrease_item, name="decrease_item"),
    path('remove_item/<int:cart_item_id>/', views.remove_cart_item, name="remove_item"),
]
