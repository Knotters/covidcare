from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('call/<str:argv>',views.callCommand),
    path('<str:need>', views.needs),
]
