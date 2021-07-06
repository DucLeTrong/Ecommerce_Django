import datetime

from django import forms
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from store.models import Product


# Create your views here.

def payments(request):
    return render(request, 'orders/payments.html')

def make_payment(request):
    if request.method == 'POST':
        data = request.POST
        order_id = data['orderID']

        time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        trans_id = order_id + "_" + time_now
        payment_method = data['payment_method']
        amount_paid = data['amount']
        status = data['status']

        

        payment = Payment(
            user = request.user,
            payment_id = trans_id,
            payment_method = payment_method,
            amount_paid = amount_paid,
            status = status

        )
        payment.save()

        order = Order.objects.get(order_number=order_id)
        order.payment = payment
        order.is_ordered = True
        order.save()

        # print(order_id, payment_method, amount_paid, status)

        # Move the cart items to Order Product table 
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
            
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            # orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()
        
        # Clear Cart
        CartItem.objects.filter(user=request.user).delete()


    return HttpResponse('ok')


def place_order(request, total = 0, quantity = 0):
    current_user = request.user

    # If the cart count is less than or equal to 0, the redirect  back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = total * 10 / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store 
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")

            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))


            d = datetime.date(yr, mt, dt)

            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            # time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # order_number = time_now + str(data.id)
            print(order_number)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,
                                     is_ordered=False,
                                    order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    return redirect('checkout')
