from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/shorten/', views.shorten_url, name='shorten'),
    path('stats/<str:code>', views.stats, name='stats'),
    path('<str:code>', views.redirect_url, name='redirect'),
]