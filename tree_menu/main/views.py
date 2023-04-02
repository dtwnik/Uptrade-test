from django.shortcuts import render
from .models import Menu


def allmenu(request):
    menu_items = Menu.objects.all()
    context = {'menu': menu_items}
    return render(request, 'main/index.html', context)


def menu_page(request, menu_name):
    menu = Menu.objects.filter(name=menu_name).prefetch_related('children').first()
    print(menu.name)
    return render(request, 'main/menu.html', {'menu': menu})
