from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect


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