from pdf_downloaders import HarvardPDFDownloader
from os import listdir, path
from subprocess import check_output
from log_parser import HarvardLogParser
from police_logs import HarvardPoliceLog
import requests
import logging

TEMP_PDF_DIR = 'temp_data/'

HarvardPDFDownloader().run(TEMP_PDF_DIR)
pdf_names = listdir(TEMP_PDF_DIR)
if len(pdf_names) > 0:
    log_texts = [check_output(['pdftotext', path.join(TEMP_PDF_DIR, pdf_name), '-']) for pdf_name in pdf_names
                 if pdf_name.endswith('.pdf')]
    lp = HarvardLogParser()
    unflattened_police_logs = [lp.parse(text=log_text) for log_text in log_texts]
    police_logs = [log for log_list in unflattened_police_logs for log in log_list]
    for log_json in map(lambda log: log.to_json(), police_logs):
        result = requests.post('http://localhost:8000/internal/create/', data=log_json)
        logging.debug("Got %d after POSTing %s" % (result.status_code, log_json))
