from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category


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
    return render(request, 'catalog/product.html', locals())





