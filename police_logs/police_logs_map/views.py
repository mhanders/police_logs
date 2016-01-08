from django.shortcuts import render
from django.template import Template, Context, loader
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import PoliceLog, deserialize_to_police_log
from dateutil.parser import parse
import ipdb

EXISTING_POLICE_LOG_REPORT_MSG = 'Error 400: PoliceLogReport with overlapping dates already exists'

@require_http_methods(['GET'])
def index(request):
	context = Context({'police_logs': PoliceLog.objects.all()})
	return render(request, 'map.html', context)

@require_http_methods(['GET'])
def last_report(request):
	logs = PoliceLog.objects.order_by('datetime_reported')
	assert(len(logs) > 0)
	return HttpResponse(logs.last().datetime_reported.date())

@csrf_exempt
@require_http_methods(['POST'])
def create(request):
	police_log = deserialize_to_police_log(request.POST)
	police_log.save()
	return HttpResponse(status=200)