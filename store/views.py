from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product

from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
# Create your views here.

def store(request, category_slug=None):

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
    context = {
        "products" : products
    }
    return render(request, "store/store.html", context)

def product_detail(request, category_slug = None, product_slug=None):

    in_cart = False
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        "single_product" : single_product, 
        "in_cart"        : in_cart,
    }

    return render(request, "store/product_detail.html", context)