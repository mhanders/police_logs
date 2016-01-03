from django.shortcuts import render
from django.template import Template, Context, loader
from django.http import HttpResponse
from models import PoliceLog
import ipdb

def index(request):
	context = Context({'police_logs': PoliceLog.objects.all()})
	return render(request, 'map.html', context)
