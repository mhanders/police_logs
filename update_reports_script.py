from harvard_log_parser import HarvardPoliceLogParser
import requests
import ipdb

parser = HarvardPoliceLogParser()
logs = parser.parse('sample_2page.txt')
log = logs[0]
# print map(lambda x: x.to_json(), logs)

print requests.post('http://localhost:8000/internal/create/', data=log.to_json()).text[:10100]