from django.contrib import admin
from django.urls import path, include
from . import env, views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(env.ADMINPATH, admin.site.urls),
    path('', views.index),
    path('needs/', include('needs.urls')),
    path('sheets/', include('gsheets.urls')),
    path('volunteer', views.volunteer)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
