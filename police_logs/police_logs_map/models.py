from django.db import models
from dateutil.parser import parse
import ipdb

class PoliceLogReport(models.Model):
	date_from = models.DateTimeField()
	date_to = models.DateTimeField()
	authority = models.CharField(max_length=20)

class PoliceLog(models.Model):
	datetime_reported = models.DateTimeField()
	datetime_occurred = models.DateTimeField()
	incident_type 	  = models.CharField(max_length=50)
	address 		  = models.CharField(max_length=300)
	lat 			  = models.FloatField()
	lng 			  = models.FloatField()
	detail			  = models.TextField()
	authority		  = models.CharField(max_length=20)

	report 			  = models.ForeignKey(PoliceLogReport, 
							on_delete=models.SET_NULL, 
							null=True)

def deserialize_to_police_log(data):
	datetime_reported = parse(data['datetime_reported'])
	report_set = PoliceLogReport.objects.filter(
		date_from__lte=datetime_reported.date()
		).filter(date_to__gte=datetime_reported.date())
	assert(report_set.count() < 2)
	
	if report_set.count() == 0:
		assert(PoliceLogReport.objects.order_by(
			'date_to'
			).last().date_to <= datetime_reported)
	else:
		report = report_set.first()
		return PoliceLog(
			datetime_reported=parse(data['datetime_reported']),
			datetime_occurred=parse(data['datetime_occurred']), 
			incident_type=data['incident_type'],
			address=data['address'], lat=data['lat'], lng=data['lng'],
			detail=data['detail'], authority=data['authority'], 
			report=report)