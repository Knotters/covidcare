import uuid
from django.db import models
from datetime import datetime

class NeedType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    about = models.CharField(max_length=100, default='Browse sources including volunteer verified ones.')
    icon = models.CharField(max_length=100,default='info')
    def __str__(self):
        return self.type

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    needtype = models.ForeignKey(NeedType, on_delete=models.CASCADE)
    provider = models.CharField(max_length=1000)
    location = models.CharField(max_length=2000,default='N/A')
    contact = models.CharField(max_length=1000,null=False,blank=False)
    lastverified = models.DateTimeField(default=datetime.now())
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.provider} for {self.needtype}'