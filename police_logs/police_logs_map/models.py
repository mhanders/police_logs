from django.db import models

class PoliceLog(models.Model):
	datetime_reported = models.DateTimeField()
	datetime_occurred = models.DateTimeField()
	incident_type = models.CharField(max_length=50)
	address = models.CharField(max_length=300)
	lat = models.FloatField()
	lng = models.FloatField()
	detail = models.TextField()
	authority = models.CharField(max_length=20)