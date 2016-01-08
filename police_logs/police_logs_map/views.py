from django.shortcuts import render
from django.template import Template, Context, loader
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import PoliceLog, PoliceLogReport, deserialize_to_police_log
from dateutil.parser import parse
import ipdb

EXISTING_POLICE_LOG_REPORT_MSG = 'Error 400: PoliceLogReport with overlapping dates already exists'

@require_http_methods(['GET'])
def index(request):
	context = Context({'police_logs': PoliceLog.objects.all()})
	return render(request, 'map.html', context)

@require_http_methods(['GET'])
def last_report(request):
	reports = PoliceLogReport.objects.order_by('date_to')
	assert(len(reports) > 0)
	return HttpResponse(reports.last().date_to.date())

@csrf_exempt
@require_http_methods(['POST'])
def create(request):
	police_log = deserialize_to_police_log(request.POST)
	police_log.save()
	return HttpResponse(status=200)

@csrf_exempt
@require_http_methods(['POST'])
def create_report(request):
	date_from = parse(request.POST['date_from']).date()
	date_to = parse(request.POST['date_to']).date()
	authority = request.POST['authority']

	if PoliceLogReport.objects.filter(date_from__exact=date_from, date_to__exact=date_to).exists():
		return HttpResponse(EXISTING_POLICE_LOG_REPORT_MSG, status=400)
	
	report = PoliceLogReport(date_from=date_from, 
		date_to=date_to, 
		authority=authority)
	
	report.save()
	return HttpResponse(status=200)