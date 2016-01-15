import sys
import logging
import numpy as np
import requests
from dateutil.parser import parse
from datetime import datetime

API_URL = 'http://localhost:8000/last_report'
HUPD_PDF_LINK = "http://www.hupd.harvard.edu/files/hupd/files/%s.pdf"
LOG_PDF_NAME = "HUPD_LOG_%s.pdf"


class HarvardPDFDownloader(object):

    def __init__(self):
        self.logger = self._get_logger()

    @staticmethod
    def _get_logger():
        logger = logging.getLogger('pdf_script_logger')
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)
        logger.setLevel(logging.INFO)
        return logger

    def _save_pdf_from_link(self, url, rel_dir, date):
        filename = LOG_PDF_NAME % date.strftime("%m-%d-%Y")
        response = requests.get(url)
        if response.status_code == 200:
            with open(rel_dir + filename, 'wb') as f:
                for data in response.iter_content():
                    f.write(data)
                self.logger.info("PDF written successfully")
        else:
            self.logger.info("404 on log with date %s" % date.strftime("%m-%d-%Y"))

    def run(self, temp_pdf_dir):
        last_report_resp = requests.get(API_URL).text
        assert last_report_resp
        last_report_date = parse(last_report_resp).date()
        self.logger.info("Got last date as " + str(last_report_date))

        date_range = np.arange(last_report_date, np.datetime64('today')).astype(datetime)
        pdf_links = map(lambda dateobj: HUPD_PDF_LINK % dateobj.strftime("%m%d%y"), date_range)

        for link, date in zip(pdf_links, date_range):
            self.logger.info("Attempting to download log from %s" % date.strftime("%m-%d-%Y"))
            self._save_pdf_from_link(link, temp_pdf_dir, date)

if __name__ == '__main__':
    HarvardPDFDownloader().run('temp_data/')