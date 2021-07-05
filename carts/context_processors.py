from django.shortcuts import resolve_url
from .models import Cart, CartItem
from .views import _cart_id

def count_items(request):

    if 'admin' in request.path:
        return {}

    cart_count  = 0

    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            # cart_items = CartItem.objects.all().filter(user=request.user)
            cart_items = CartItem.objects.all().filter(user=request.user)
            print(len(cart_items))
        else:
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
    
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        pass

    return {"cart_count" : cart_count}
    # cart_count = 0
    # if 'admin' in request.path:
    #     return {}
    # else:
    #     try:
    #         cart = Cart.objects.filter(cart_id=_cart_id(request))
    #         if request.user.is_authenticated:
    #             cart_items = CartItem.objects.all().filter(user=request.user)
    #         else:
    #             cart_items = CartItem.objects.all().filter(cart=cart[:1])
    #         for cart_item in cart_items:
    #             cart_count += cart_item.quantity
    #     except Cart.DoesNotExist:
    #         cart_count = 0
    # return dict(cart_count=cart_count)