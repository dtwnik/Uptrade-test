from django import template
from django.template.defaultfilters import safe
from django.urls import reverse
from django.utils.html import format_html, urlize

from ..models import Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    active_url = request.path_info
    menu_items = Menu.objects.filter(name=menu_name).prefetch_related('children')

    def render_menu_items(menu_items):
        result = []
        for menu_item in menu_items:
            is_active = active_url.startswith(menu_item.url)
            has_children = menu_item.children.exists()

            if is_active:
                css_class = 'active'
            else:
                css_class = ''

            if has_children:

                result.append(f'<li class="{css_class}"><a href="{menu_item.url}">{menu_item.name}</a><ul>')
                result.append(render_menu_items(menu_item.children.all()))
                result.append('</ul></li>')
            else:
                result.append(f'<li class="{css_class}"><a href="{menu_item.url}">{menu_item.name}</a></li>')

        return format_html(''.join(result))

    return render_menu_items(menu_items)


# @register.simple_tag(takes_context=True)
# def draw_menu(context, menu_name):
#     request = context['request']
#     current_url = request.path
#     menu_items = Menu.objects.filter(parent=None, menu=menu_name).prefetch_related('children')
#     return render_menu_items(menu_items, current_url)
#

# def render_menu_items(menu_items, current_url):
#     result = []
#     for menu_item in menu_items:
#         css_class = 'active' if current_url == menu_item.url else ''
#         has_children = menu_item.children.exists()
#
#         if has_children:
#             result.append(f'<li class="{css_class}"><a href="{menu_item.url}">{menu_item.name}</a><ul>')
#             result.append(render_menu_items(menu_item.children.all(), current_url))
#             result.append('</ul></li>')
#         else:
#             result.append(f'<li class="{css_class}"><a href="{menu_item.url}">{menu_item.name}</a></li>')
#
#     return ''.join(result)
