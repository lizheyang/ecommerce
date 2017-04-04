from django.shortcuts import render, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category
from cart import cart
from cart.forms import AddToCartForm


def index(request):
    categories = Category.objects.all()
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 4)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())


def show_categories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(categories__id=category_id)
    return render(request, 'catalog/category.html', locals())


def show_product(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    categories = p.categories.all()
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = AddToCartForm(request, postdata)
        if form.is_valid():
            cart.add_to_cart(request)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
        else:
            render(request, 'test.html', locals())
    else:
        form = AddToCartForm(request=request, label_suffix=':')
        form.fields['product_id'].widget.attrs['value'] = product_id
        request.session.set_test_cookie()
        return render(request, 'catalog/product.html', locals())





