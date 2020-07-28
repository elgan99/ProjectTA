# from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django_mongoengine import mongo_admin
# from otomasiACL.views import IPListView

urlpatterns = [
    path('', views.home, name='otomasi-acl'),
    # path("ip/", IPListView.as_view(template_name='otomasiAcl/ip.html'), name='ip')
]
