import ipdb
from log_parser import LogParser
from police_logs import HarvardPoliceLog


class HarvardPoliceLogParser(LogParser):

    def __init__(self):
        super(HarvardPoliceLogParser, self).__init__(HarvardPoliceLog)

if __name__ == '__main__':
    print HarvardPoliceLogParser().parse('sample_2page.txt')