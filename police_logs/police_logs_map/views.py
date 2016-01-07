from django.shortcuts import render
from django.template import Template, Context, loader
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from models import PoliceLog, serialize_to_policelog
import ipdb

@require_http_methods(['GET'])
def index(request):
	context = Context({'police_logs': PoliceLog.objects.all()})
	return render(request, 'map.html', context)

@require_http_methods(['POST'])
def create(request):
	data = request.POST['police_log']
	police_log = deserialize_to_policelog(data)
	police_log.save()

@require_http_methods(['POST'])
def create_report(request):
	date_from = request.POST['date_from']
	date_to = request.POST['date_to']
	authority = request.POST['authority']
	report = PoliceLogReport(date_from=date_from, 
		date_to=date_to, 
		authority=authority)
	report.save()