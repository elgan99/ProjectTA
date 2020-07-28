from django.shortcuts import render
from django.http  import HttpResponse
from django.views.generic import ListView
from .models import IP
from .tables import IPTable
import yaml
# from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
# from dj_ansible.ansible_kit import execute
import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



posts = [
    {
    'author': 'Elgan',
    'title': 'daftar Access-List',
    'content': 'List',
    'date_posted': 'July 19, 2020'
    },
    {
    'author': 'Elgan',
    'title': 'Hapus Access-List',
    'content': 'List',
    'date_posted': 'July 19, 2020'
    },
]

# Create your views here.

def home(request):
    ip = IP.objects.all()
    context = {
        'posts': posts,
        'ip':ip
    }
    return render(request, 'otomasiAcl/home.html', context)


def acl(request):
    ip = IP.objects.all()
    output = []
    my_group = AnsibleNetworkGroup(name='acl_config',
                            ansible_connection='network_cli',
                            ansible_network_os='ios',
                            ansible_become=True)
    my_group.save()
    host = AnsibleNetworkHost(host='Router2',
                            ansible_ssh_host='192.168.56.120',
                            ansible_user='elgan',
                            ansible_ssh_pass='123',
                            ansibel_become_pass='123',
	                        group=my_group)
    host.save()

    # client = MongoClient()
    # db = client['HP']
    # collection = db.hacker
    # for ip in collection.find({}, {'Ip_Address':1, '_id':0}).sort([('_id',1)]).limit(1):
    #          print(ip['Ip_Address'])
    my_play= dict(
             name="acl_config",
             hosts='Router2',
             become='yes',
             become_method='enable',
             gather_facts='no',
             tasks=[
                dict(action=dict(module='ios_config',lines=['access-list 120 deny tcp any any eq 23']))])
    
    result = execute(my_play)
    output = json.dumps(result.results, indent=4)
    context = {
        'ip': ip,
        'output' :output
        # 'result':result
    }
    return render(request, 'otomasiAcl/home.html', context)



    
