import uuid
from django.db import models
from datetime import datetime
from gsheets import mixins

def needTypeImgPath(instance, filename):
    return 'needs/types/{}/'.format(str(instance.type))+'/{}'.format(filename)


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sid = models.IntegerField(default=1)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    did = models.IntegerField(default=1)
    name = models.CharField(max_length=150)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.state.name} - {self.name}'


class NeedType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    about = models.CharField(
        max_length=100, default='Browse sources including volunteer verified ones.')
    image = models.FileField(upload_to=needTypeImgPath,null=True, blank=True, max_length=500)

    def __str__(self):
        return self.type


class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    needtype = models.ForeignKey(NeedType, on_delete=models.CASCADE)
    provider = models.CharField(max_length=1000)
    contact = models.CharField(max_length=1000, null=False, blank=False)
    address = models.CharField(max_length=2000, default='N/A')
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    lastupdate = models.DateTimeField(default=datetime.now())
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.provider} for {self.needtype}'


class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msg = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.msg

class Phoneline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=1000)
    number = models.CharField(max_length=100)
    
    def __str__(self):
        return self.text

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

class Infi(mixins.SheetSyncableMixin,models.Model):
    speadsheet_id = "1IXpZEpGFzJfT7kJ5Kk_P6MPyBseS2xvFDkxcK064NqU"
    model_id_field = 'id'
    sheet_id_field = "id"
    id = models.UUIDField(primary_key=True,editable=False)
    question = models.CharField(max_length=5000)
    link = models.CharField(max_length=1000)
