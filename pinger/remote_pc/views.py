from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DS
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    dss = DS.objects.all()
    content = {
        'dss': dss,
    }
    return render(request, 'remote_pc/index.html', content)

@require_http_methods(['GET'])
def ping_ds(request, ds_name):
    try:
        ds = DS.objects.get(name=ds_name)
    except DS.DoesNotExist:
        return HttpResponse('Incorrect DS name', status=404)
    ds.ping()
    return HttpResponse('Ping success')

