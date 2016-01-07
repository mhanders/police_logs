class PoliceLog(object):

	def to_json(self):
		raise NotImplementedError()

class HarvardPoliceLog(PoliceLog):

	def __init__(self, data):
		self.datetime_reported = data[0]
		self.incident_type = data[1]
		self.datetime_occurred = data[2]
		self.address = data[3]
		self.disposition = data[4]
		self.detail = data[5]

	def to_json(self):
		return {
			'datetime_reported': self.datetime_reported,
			'datetime_occurred': self.datetime_occurred,
			'incident_type': self.incident_type,
			'address': self.address,
			'disposition': self.disposition,
			'detail': self.detail,
			'authority': 'HARVARD'
		}