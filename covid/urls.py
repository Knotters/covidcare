from django.contrib import admin
from django.urls import path, include
from . import env, views

urlpatterns = [
    path(env.ADMINPATH, admin.site.urls),
    path('', views.index),
    path('needs/', include('needs.urls'))
]
