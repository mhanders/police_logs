from urllib2 import urlopen
from bs4 import BeautifulSoup
from dateutil.parser import parse

API_URL = 'http://localhost:8000/last_report'
HUPD_LOGS_LINK = 'http://www.hupd.harvard.edu/public-police-log'
LOG_PDF_NAME = "HUPD_LOG_%s.pdf"


def save_pdf_from_link(url, date):
    filename = LOG_PDF_NAME % date.strftime("%m-%d-%Y")
    with open('log_pdfs/%s' % filename, 'wb') as f:
        for data in urlopen(url).read():
            f.write(data)

last_report_resp = urlopen(API_URL)
assert last_report_resp
last_report_date = parse(last_report_resp.read()).date()
print "Got last date as " + str(last_report_date)

hupd_logs_site = urlopen(HUPD_LOGS_LINK)
bsobj = BeautifulSoup(hupd_logs_site, 'html.parser')

file_divs = bsobj.find_all('div', {'class': 'file-info'})
for file_div in file_divs:
    report_date = parse(file_div.find('a', {'class': 'entity-link'}).get_text()).date()
    if report_date > last_report_date:
        download_link = file_div.find('a', {'class': 'download-link'}).get('href')
        print "Attempting to download file from %s" % download_link
        save_pdf_from_link(download_link, report_date)
        print "Successfully downloaded!!"
