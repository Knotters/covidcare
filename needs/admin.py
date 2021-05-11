from django.contrib import admin
from .models import Lead,NeedType,Alert, Latest, Video,FAQ

admin.site.register(NeedType)
admin.site.register(Lead)
admin.site.register(Alert)
admin.site.register(Latest)
admin.site.register(Video)
admin.site.register(FAQ)