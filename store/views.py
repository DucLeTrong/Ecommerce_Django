from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
# Create your views here.
def store(request, category_slug=None):

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category,is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
    context = {
        "products" : products
    }
    return render(request, "store/store.html", context)