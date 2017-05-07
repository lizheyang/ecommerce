from django.shortcuts import render, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.models import Product, Category, Comment
from catalog.form import AddCommentForm
from cart import cart
from cart.forms import AddToCartForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from datetime import date


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
            form = AddToCartForm(request=request, label_suffix=':')
            form.fields['product_id'].widget.attrs['value'] = product_id
            comment_form = AddCommentForm(request=request)
            # comment_form.fields['product_id'].widget.attrs['value'] = product_id
            # comment_form.fields['author_id'].widget.attrs['value'] = request.user.id
            comments = Comment.objects.filter(product__id=product_id)
            request.session.set_test_cookie()
            return render(request, 'catalog/product.html', locals())
    else:
        form = AddToCartForm(request=request, label_suffix=':')
        form.fields['product_id'].widget.attrs['value'] = product_id
        comment_form = AddCommentForm(request=request)
        # comment_form.fields['product_id'].widget.attrs['value'] = product_id
        # comment_form.fields['author_id'].widget.attrs['value'] = request.user.id
        comments = Comment.objects.filter(product__id=product_id)
        request.session.set_test_cookie()
        return render(request, 'catalog/product.html', locals())


@login_required
def add_comment(request):
    try:
        if request.method == 'POST':
            postdata = request.POST.copy()
            form = AddCommentForm(request, postdata)
            if form.is_valid():
                product_id = postdata.get('product_id', -1)
                author_id = postdata.get('author_id', -1)
                p = get_object_or_404(Product, id=int(product_id))
                au = get_object_or_404(User, id=int(author_id))
                comment = Comment()
                comment.content = postdata.get('content', '')
                comment.author = au
                comment.product = p
                comment.save()
                # url = urlresolvers.reverse('product', args=(p.id,))
                # return HttpResponseRedirect(url)
                date_now = date.today().strftime('%y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
                return HttpResponse(json.dumps({'success': True, 'message': '',
                                                'comment': {
                                                    'author': comment.author.username,
                                                    'content': comment.content,
                                                    'date': date_now,
                                                }}),
                                    content_type="application/json"
                                    )
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'message': e,
                                        'comments_list': []}),
                            content_type = "application/json"
                            )

