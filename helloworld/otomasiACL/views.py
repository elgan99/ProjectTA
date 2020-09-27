from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.views.generic import ListView
from .models import IP
# from .tables import IPTable
import yaml
from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
from dj_ansible.ansible_kit import execute
import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import threading


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
    if request.method == 'GET' and 'btnform1' in request.GET:
        print("berhasil")
        my_group=AnsibleNetworkGroup.objects.all()
        host=AnsibleNetworkHost.objects.all()
        t1 = threading.Thread(target=acl, args=[my_group,host])
        t1.start()
    context = {
        'posts': posts,
        'ip':ip
    }
    return render(request, 'otomasiAcl/home.html', context)


def acl(my_group,host):
    #ip = IP.objects.values_list('Ip', flat=True
    print("Starting Config ACL!")
    jumlah = IP.objects.count()
    ulang = True
    while ulang :
        jumlah2 = IP.objects.count()
        if jumlah2 > jumlah:
            ulang = False
            selisih = jumlah2-jumlah
            jumlah = jumlah+selisih
            print(selisih)
            call = IP.objects.all().order_by('-id')[:selisih]
            print(call)
            ip = call.values_list('Ip', flat=True)
            for alamat in ip :
                dest = IP.objects.filter(Ip = alamat).values_list('destination', flat=True)
                for tujuan in dest:
                    port = IP.objects.filter(destination = tujuan).values_list('port', flat=True)
                    print(tujuan)
                    for port in port:
                        print(port)
                        command = ['deny tcp host '+ alamat +' host ' + tujuan + ' eq ' + port]
                        oldcommand = IP.objects.values_list('acl', flat=True)
                        sameacl= set(oldcommand).intersection(command)
                        if sameacl:
                            print("This IP already listed in Access-List")
                            ulang = True
                        else :
                            str1 = ""
                            for addacl in command:
                                str1 += addacl
                            my_play= dict(
                                    name="acl_config",
                                    hosts='testTA',
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    tasks=[
                                        dict(action=dict(module='ios_config', lines= [str1, 'permit ip any any'], parents = 'ip access-list extended 100')),
                                        # dict(action=dict(module='ios_config', lines= ['permit ip any any'], parents = 'ip access-list extended 100')),
                                        dict(action=dict(module='ios_config', lines= ['ip access-group 100 in'], parents = 'int g0/0'))
                                        ])
                            result = execute(my_play)
                            hasil = result.stats
                            kond = hasil['hosts'][0]['status']
                            if kond == 'ok':
                                print(result.stats)
                                IP.objects.filter(Ip = alamat).update(acl = str1)
                            else:
                                print(result.results)
                                print('fail')
            ulang = True
    context = {
        'ip': alamat,
        'acl': command,
    }
    return render(request, 'otomasiAcl/home.html', context)

def deleteIp(request, id):
    cari = IP.objects.get(pk = id )
    ip = cari.Ip
    command = cari.acl
    num= cari.NumId
    # str1 = ""
    # for remove in command:
    #     str1 += remove
    my_play= dict(
            name="acl_config",
            hosts='testTA',
            become='yes',
            become_method='enable',
            gather_facts='no',
            tasks=[
                    dict(action=dict(module='ios_config', lines= ["no " + command], parents = 'ip access-list extended 100'))
                    ])
    result = execute(my_play)
    cari.delete()
    print(result.stats)
    return redirect('otomasi-acl')





