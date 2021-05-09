from django.contrib import admin
from .models import Lead,NeedType
# Register your models here.

admin.site.register(NeedType)
admin.site.register(Lead)