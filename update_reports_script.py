from harvard_log_parser import HarvardPoliceLogParser
import requests
import ipdb

parser = HarvardPoliceLogParser()
logs = parser.parse('sample_2page.txt')
logs_as_json = map(lambda x: x.to_json(), logs)

for log_json in logs_as_json:
	requests.post('http://localhost:8000/internal/create/', data=log_json)