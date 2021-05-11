import uuid
from django.db import models
from datetime import datetime

def needTypeImgPath(instance,filename):
    return 'needs/types/{}/'.format(str(instance.type))+'/{}'.format(filename)

class NeedType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    about = models.CharField(max_length=100, default='Browse sources including volunteer verified ones.')
    image = models.FileField(upload_to=needTypeImgPath,null=True,blank=True,max_length=500)

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


class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msg = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.msg

class Latest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000, null=True, blank=True)
    updatedAt = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.content

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        if self.title == None:
            return self.link
        return self.title

class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=5000)

    def __str__(self):
        return self.question
    