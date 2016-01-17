from dateutil.parser import parse
import re
import geocoder
import time

MAX_GEOCODE_RETRIES = 2
GEOCODE_NO_RESULTS_STATUS = 'ZERO_RESULTS'
GEOCODE_TOO_MANY_QUERIES_STATUS = 'OVER_QUERY_LIMIT'
DEFAULT_GEOCODE_RETURN = [None, None]


class PoliceLog(object):

    date_reg = r'(?:0|1)[0-2]/[0-3]?[0-9]/[0-3][0-9]'
    time_reg = r'(?:(?:1?[0-2])|[0-9]):[0-9]{2}\s(?:A|P)M'
    datetime_reg = re.compile(date_reg + '\s*-?\s*' + time_reg)

    @staticmethod
    def parse_datetime_occurred(datetime_str):
        datetimes = PoliceLog.datetime_reg.findall(datetime_str)
        assert(len(datetimes) > 0)
        return parse(datetimes[0])

    @staticmethod
    def latlng(address, tries=0):
        if tries == MAX_GEOCODE_RETRIES:
            return DEFAULT_GEOCODE_RETURN
        result = geocoder.google(address)
        if result.status == GEOCODE_NO_RESULTS_STATUS:
            split_address = address.split(' ')

            # Really, an address needs more than 3 words
            # might even want to move this logic higher up the chain.. see what real plots look like first
            if len(split_address) > 3:
                return PoliceLog.latlng(' '.join(split_address[1:]))
            return DEFAULT_GEOCODE_RETURN

        if result.status_code != 200 or result.status == GEOCODE_TOO_MANY_QUERIES_STATUS:
            time.sleep(3)
            return PoliceLog.latlng(address, tries=tries+1)

        return result.latlng

    def to_json(self):
        raise NotImplementedError()


class HarvardPoliceLog(PoliceLog):

    dispositions = ['CLOSED', 'OPEN', 'ARREST']

    def __init__(self, data):
        self.datetime_reported = parse(data[0])
        self.incident_type = data[1]
        self.datetime_occurred = PoliceLog.parse_datetime_occurred(data[2])
        self.address = data[3]
        self.latlng = PoliceLog.latlng(self.address)
        self.disposition = data[4]
        self.detail = data[5]

    def to_json(self):
        return {
            'datetime_reported': self.datetime_reported.isoformat(),
            'datetime_occurred': self.datetime_occurred.isoformat(),
            'incident_type': self.incident_type,
            'address': self.address.replace('\n', ','),
            'lat': self.latlng[0],
            'lng': self.latlng[1],
            'disposition': self.disposition,
            'detail': self.detail,
            'authority': 'HARVARD'
        }
