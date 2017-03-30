from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from .forms import UserProfileForm
from .models import UserProfile


def register(request):
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
    return render(request, 'accounts/my_account.html', locals())


@login_required
def edit_profile(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserProfileForm(postdata)
        if form.is_valid():
            setprofile(request)
            url = urlresolvers.reverse('show_profile')
            return HttpResponseRedirect(url)
    else:
        user_profile = retrieve(request)
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/edit_profile.html', locals())


@login_required
def show_profile(request):
    profile = retrieve(request)
    return render(request, 'accounts/show_profile.html', locals())



def retrieve(request):
    try:
        profile = get_object_or_404(UserProfile, user=request.user)
    except:
        profile = UserProfile(user=request.user)
        profile.save()
    return profile


def setprofile(request):
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()