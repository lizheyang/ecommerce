import os
from PIL import Image
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from ecommerce.settings import MEDIA_ROOT
from .forms import UserProfileForm, UserAddressForm, UserFeedbackForm
from .models import UserProfile, UserAddress, UserCollection, UserFeedback
from orders.models import Order
from menus.models import Menu
from .utils import get_my_collections


def register(request):
    if request.user.is_authenticated():
        url = urlresolvers.reverse('my_account')
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            username = postdata.get('username', '')
            passwd = postdata.get('password1', '')
            new_user = authenticate(username=username, password=passwd)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', locals())


@login_required
def my_account(request):
    my_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
    menus = get_my_collections(request)[:3]
    return render(request, 'accounts/my_account.html', locals())


@login_required
def edit_profile(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            setprofile(request)
            url = urlresolvers.reverse('show_profile')
            if request.FILES.get('photo'):
                photo = request.FILES['photo']
                photo_ext = str(photo).split('.')[-1]
                photo_name = '%s.%s'%(request.user.username, photo_ext)
                img = Image.open(photo)
                img_path = os.path.join(MEDIA_ROOT, 'accounts')
                img_name = os.path.join(img_path, photo_name)
                img.save(img_name)
                count = UserProfile.objects.filter(user=request.user).update(
                    photo='accounts/' + photo_name
                )
                if count:
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponse('头像上传失败')
            return HttpResponseRedirect(url)
    else:
        user_profile = retrieve(request)
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/edit_profile.html', locals())


@login_required
def show_profile(request):
    profile = retrieve(request)
    return render(request, 'accounts/show_profile.html', locals())


@login_required
def my_password_change_done(request, current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return render(request, 'accounts/pw-change-down.html', context)


def retrieve(request):
    # 根据request查找用户profile，如果还没有则创建
    try:
        profile = get_object_or_404(UserProfile, user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()
    return profile


def setprofile(request):
    # 根据request查找用户profile,然后实例化ProfileFrom
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()


@login_required
def show_address(request):
    addresses = UserAddress.objects.filter(user=request.user)
    return render(request, 'accounts/show_address.html', locals())


@login_required
def add_address(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserAddressForm(postdata)
        if form.is_valid():
            address = UserAddress()
            address.user = request.user
            address.receiver_name = postdata.get('receiver_name', '')
            address.receiver_phone = postdata.get('receiver_phone', '')
            address.province = postdata.get('province', '')
            address.city = postdata.get('city', '')
            address.area = postdata.get('area', '')
            address.detail_addr = postdata.get('detail_addr', '')
            address.post_code = postdata.get('post_code', '')
            address.save()
            url = urlresolvers.reverse('show_address')
            return HttpResponseRedirect(url)
    else:
        form = UserAddressForm()
    return render(request, 'accounts/add_address.html', locals())


@login_required
def show_orders(request):
    my_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/show_orders.html', locals())


@login_required
def show_collections(request):
    menus = get_my_collections(request)
    return render(request, 'accounts/show_collections.html', locals())


@login_required
def add_collection(request, menu_folder):
    collection = UserCollection()
    collection.menu = Menu.objects.get(folder_name=menu_folder)
    collection.user = request.user
    collection.save()
    url = urlresolvers.reverse('show_collections')
    return HttpResponseRedirect(url)


@login_required
def delete_collection(request, menu_folder):
    menu = Menu.objects.get(folder_name=menu_folder)
    collection = UserCollection.objects.get(menu=menu, user=request.user)
    collection.delete()
    url = urlresolvers.reverse('show_collections')
    return HttpResponseRedirect(url)


@login_required
def add_feedback(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserFeedbackForm(postdata)
        if form.is_valid():
            feedback = UserFeedback()
            feedback.user = request.user
            feedback.title = postdata.get('title')
            feedback.content = postdata.get('content')
            feedback.reply = ''
            feedback.status_code = 1
            feedback.save()
            url = urlresolvers.reverse('show_feedbacks')
            return HttpResponseRedirect(url)
    else:
        form = UserFeedbackForm()
        return render(request, 'accounts/add_feedback.html', locals())


@login_required
def show_feedbacks(request):
    feedbacks = UserFeedback.objects.filter(user=request.user)
    return render(request, 'accounts/show_feedbacks.html', locals())


@login_required
def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(UserFeedback, id=feedback_id)
    return render(request, 'accounts/feedback_detail.html', locals())