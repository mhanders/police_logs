from dateutil.parser import parse
import re
import geocoder
import ipdb

date_reg = '(?:0|1)[0-2]/[0-3][0-9]/[0-3][0-9]'
time_reg = '(?:(?:1?[0-2])|[0-9]):[0-9]{2}\s(?:A|P)M'
datetime_reg = re.compile(date_reg + '\s*-?\s*' + time_reg)


def parse_datetime_occurred(datetime_str):
    datetimes = datetime_reg.findall(datetime_str)
    assert(len(datetimes) > 0)
    return parse(datetimes[0])


def latlng(address):
    return geocoder.google(address).latlng


class PoliceLog(object):

    def to_json(self):
        raise NotImplementedError()


class HarvardPoliceLog(PoliceLog):

    def __init__(self, data):
        self.datetime_reported = parse(data[0])
        self.incident_type = data[1]
        self.datetime_occurred = parse_datetime_occurred(data[2])
        self.address = data[3]
        self.latlng = latlng(self.address)
        self.disposition = data[4]
        self.detail = data[5]

    def to_json(self):
        return {
            'datetime_reported': self.datetime_reported.isoformat(),
            'datetime_occurred': self.datetime_occurred.isoformat(),
            'incident_type': self.incident_type,
            'address': self.address,
            'lat': self.latlng[0],
            'lng': self.latlng[1],
            'disposition': self.disposition,
            'detail': self.detail,
            'authority': 'HARVARD'
        }
