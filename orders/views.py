from django.shortcuts import render, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from cart import cart
from accounts.models import UserAddress
from .models import Order, OrderItem
from .util import generate_order_id


def checkout(request):
    if request.method == 'POST':
        pass
    cart_items = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)
    address_list = UserAddress.objects.filter(user=request.user)
    return render(request, 'orders/checkout.html', locals())


def create_order(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        address_id = int(postdata.get('address_id', "-1"))
        order = Order()
        order.user = request.user
        order.address = get_object_or_404(UserAddress, id=address_id)
        order.id = generate_order_id()
        order.status = 1
        order.save()
        if order.pk:
            cart_items = cart.get_cart_items(request)
            for item in cart_items:
                oi = OrderItem()
                oi.order = order
                oi.quantity = item.quantity
                oi.price = item.price()
                oi.product = item.product
                oi.save()
            cart.empty_cart(request)
            url = urlresolvers.reverse('order_page', args=(order.id,))
            return HttpResponseRedirect(url)


def order_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_page.html', locals())



