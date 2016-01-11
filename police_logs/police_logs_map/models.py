from django.db import models
from dateutil.parser import parse


class PoliceLog(models.Model):
    datetime_reported = models.DateTimeField()
    datetime_occurred = models.DateTimeField()
    incident_type = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    lat = models.FloatField()
    lng = models.FloatField()
    detail = models.TextField()
    authority = models.CharField(max_length=20)

    class Meta:
        unique_together = ('datetime_reported',
                           'datetime_occurred', 'address', 'detail')


def deserialize_to_police_log(data):
    return PoliceLog(
        datetime_reported=parse(data['datetime_reported']),
        datetime_occurred=parse(data['datetime_occurred']),
        incident_type=data['incident_type'],
        address=data['address'], lat=data['lat'], lng=data['lng'],
        detail=data['detail'], authority=data['authority'])
