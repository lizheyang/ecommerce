from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Menu, MenuStep
from .spider import superviser
from accounts.utils import get_my_collections


def show_menus(request):
    my_collect_menus = get_my_collections(request)
    menus_list = Menu.objects.all()
    paginator = Paginator(menus_list, 20)
    page = request.GET.get('page')
    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)
    return render(request, 'menus/show_menus.html', locals())


def menu_page(request, menu_folder):
    my_collect_menus = get_my_collections(request)
    menu = Menu.objects.get(folder_name=menu_folder)
    menu_steps = MenuStep.objects.filter(menu=menu)
    return render(request, 'menus/menu_page.html', locals())


@login_required
def spide_menus(request):
    superviser(2)
    url = urlresolvers.reverse('show_menus')
    return HttpResponseRedirect(url)


@login_required
def delete_menu(request, menu_folder):
    if request.user.has_perm('menus.delete_menu'):
        menu = Menu.objects.get(folder_name=menu_folder)
        menu_steps = MenuStep.objects.filter(menu=menu)
        for ms in menu_steps:
            ms.delete()
        menu.delete()
        url = urlresolvers.reverse('show_menus')
        return HttpResponseRedirect(url)
    else:
        return HttpResponse('您没有权限删除菜单')

