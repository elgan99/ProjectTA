import django_tables2 as tables
from .models import IP

class IPTable(tables.Table):
    class Meta:
        model = IP
        template_name = "django_tables2/bootstrap.html"
        fields = ("Ip Address", )
