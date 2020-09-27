from djongo import models
#from django.utils import timezone
# from djongo.models import forms
from mongoengine import *

#class Post(EmbeddedDocument):
#    title = fields.StringField(max_length=100)
#    content = fields.StringField()
#    date_posted = fields.DateTimeField(default=timezone.now)

# class IPTables(Document):
#     Ip = fields.StringField(max_length=100, verbose_name="Alamat IP")

class IP(models.Model):
    Ip = models.CharField(max_length=100, verbose_name="Alamat IP")
    acl = models.CharField(max_length=255, verbose_name="Konfigurasi Access-List", default="")
    destination = models.CharField(max_length=255, verbose_name="IP Tujuan", default="")
    port = models.CharField(max_length=255, verbose_name="Port", default="")
    NumId = models.CharField(max_length=255, verbose_name="NumId", default="")
    