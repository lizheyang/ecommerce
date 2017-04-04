from django.shortcuts import render
from . import cart


def show_cart(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata.get('submit') == 'Remove':
            cart.remove_from_cart(request)
        if postdata.get('submit') == 'Update':
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)
    return render(request, 'cart/cart.html', locals())
