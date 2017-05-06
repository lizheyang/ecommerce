from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from .models import Menu, MenuStep
from .spider import superviser


def show_menus(request):
    menus = Menu.objects.all()
    return render(request, 'menus/show_menus.html', locals())


def menu_page(request, menu_folder):
    menu = Menu.objects.get(folder_name=menu_folder)
    menu_steps = MenuStep.objects.filter(menu=menu)
    return render(request, 'menus/menu_page.html', locals())


@login_required
def spide_menus(request):
    superviser(2)
    url = urlresolvers.reverse('show_menus')
    return HttpResponseRedirect(url)

