from django.db import models

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
	datetime_reported = data['datetime_reported']
	report_set = PoliceLogReport.objects.filter(
		date_from__lte=datetime_reported
		).filter(date_to__gte=datetime_reported)
	assert(report_set.count() < 1)
	
	if report_set.count() == 0:
		assert(PoliceLogReport.order_by(
			'date_to__gte'
			).last().date_to < datetime_reported)
	else:
		report = report_set.first()
		return PoliceLog(
			datetime_reported=data['datetime_reported'],
			datetime_occurred=data['datetime_occurred'], 
			incident_type=data['incident_type'],
			address=data['address'], lat=data['lat'], lng=data['lng'],
			detail=data['detail'], authority=data['authority'], 
			report=report)