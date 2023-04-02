from django.urls import path

from . import views


urlpatterns = [
    path('<str:menu_name>/', views.menu_page, name='menu_page'),
]