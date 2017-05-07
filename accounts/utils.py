from menus.models import Menu
from .models import UserCollection


def get_my_collections(request):
    my_collections = UserCollection.objects.filter(user=request.user).order_by('-created_at')
    my_collect_menus = []
    if my_collections:
        my_collect_menus = [col.menu for col in my_collections]
    return my_collect_menus
