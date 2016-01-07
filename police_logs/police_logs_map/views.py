from django.shortcuts import render
from django.template import Template, Context, loader
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import PoliceLog, PoliceLogReport, deserialize_to_police_log
import ipdb
from datetime import datetime

DATE_FMT = '%m/%d/%Y'

@require_http_methods(['GET'])
def index(request):
	context = Context({'police_logs': PoliceLog.objects.all()})
	return render(request, 'map.html', context)

@csrf_exempt
@require_http_methods(['POST'])
def create(request):
	data = request.POST['police_log']
	police_log = deserialize_to_police_log(data)
	police_log.save()
	return HttpResponse(status=200)

@csrf_exempt
@require_http_methods(['POST'])
def create_report(request):
	date_from = datetime.strptime(request.POST['date_from'], DATE_FMT)
	date_to = datetime.strptime(request.POST['date_to'], DATE_FMT)
	authority = request.POST['authority']

	if PoliceLogReport.objects.filter(date_from__exact=date_from, date_to__exact=date_to).exists():
		return HttpResponse("PoliceLogReport with overlapping dates already exists", status=400)
	
	report = PoliceLogReport(date_from=date_from, 
		date_to=date_to, 
		authority=authority)
	
	report.save()
	return HttpResponse(status=200)