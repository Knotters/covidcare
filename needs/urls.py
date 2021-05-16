from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addOxygen',views.addOxygens),
    path('<str:need>', views.needs),
]
