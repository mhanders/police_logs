from django.db import IntegrityError
from django.shortcuts import render
from django.template import Context
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import PoliceLog, deserialize_to_police_log
import datetime


@require_http_methods(['GET'])
def index(request):
    police_logs = PoliceLog.objects.exclude(lat__isnull=True, lng__isnull=True)
    return render(request, 'map.html', {'police_logs': police_logs})


@require_http_methods(['GET'])
def last_report(request):
    logs = PoliceLog.objects.order_by('datetime_reported')
    if len(logs) == 0:
        return HttpResponse(datetime.datetime(2015, 11, 18).date())
    return HttpResponse(logs.last().datetime_reported.date())


@csrf_exempt
@require_http_methods(['POST'])
def create(request):
    try:
        police_log = deserialize_to_police_log(request.POST)
        police_log.save()
        return HttpResponse(status=200)
    except IntegrityError as error:
        return HttpResponse(error.message, status=422)