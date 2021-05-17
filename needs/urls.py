from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addLeads',views.addLeads),
    path('<str:need>', views.needs),
]
