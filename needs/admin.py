from django.contrib import admin
from .models import *


admin.site.register(NeedType)
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_filter = ["needtype","state"]
    list_display = ["provider", "needtype","name", "state","district"]
    def get_queryset(self,request):
        query_set = super(LeadAdmin,self).get_queryset(request)
        return query_set
    class Meta:
        ordering = ("")

admin.site.register(Alert)
admin.site.register(Latest)
admin.site.register(Video)
admin.site.register(FAQ)
admin.site.register(State)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_filter = ["state"]
    list_display = ["name", "did"]
    def get_queryset(self,request):
        query_set = super(DistrictAdmin,self).get_queryset(request)
        return query_set
    class Meta:
        ordering = ("")

@admin.register(Phoneline)
class PLAdmin(admin.ModelAdmin):
    list_display = ["text", "number"]
    def get_queryset(self,request):
        query_set = super(PLAdmin,self).get_queryset(request)
        return query_set
    class Meta:
        ordering = ("")
