#Lindsay Poirier created this script.
import re
import string
import urlparse
import requests
import csv


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

class AHV_Scraper(object):
    def scrape(self):
        # Create CSV file
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
        driver2 = webdriver.Firefox(firefox_options=options)

        f = csv.writer(open("After_Hours_Variances.csv", "w"))
        f.writerow(["AHVURL","jobNumber","referenceNumber","status","entryDate","filingType","houseNumber","streetName","borough", "BIN", "name","businessName","licenseNumber","nearResidence","enclosedBuilding","demolition","crane","requested", "approved","startDay","days","hoursFrom","hoursTo","reason","approvedReason","description"]) # Write column headers as the first line
        with open('MNCD1BINS.csv') as csvfile:
            BINList = csv.reader(csvfile)
            for BIN in BINList:
                AHVBINURL = 'http://a810-bisweb.nyc.gov/bisweb/AHVPermitsQueryByNumberServlet?requestid=1&allkey=' + str(BIN[0]) + '&fillerdata=A'
                driver2.get(AHVBINURL)
                print AHVBINURL

                while True:
                    BINHTML = driver2.page_source
                    AHVBINSoup = BeautifulSoup(BINHTML, "lxml")
                    print AHVBINSoup.title.string
                    AHVReferenceNumberTable = AHVBINSoup.findAll('table')[3]
                    print 'starting page'
                    for row in AHVReferenceNumberTable.findAll('tr')[1:]:
                        referenceNo = row.findAll('td')[0].a.string
                        AHVURL = "http://a810-bisweb.nyc.gov/bisweb/AHVPermitDetailsServlet?requestid=2&allkey=" + referenceNo
                        print AHVURL
                        #AHVRequest = requests.get(AHVURL)
                        driver.get(AHVURL)
                        AHVHTML = driver.page_source
                        AHVSoup = BeautifulSoup(AHVHTML, "lxml")
                        print AHVSoup.title.string
                        AHVTablePremises = AHVSoup.findAll('table')[2]
                        AHVTableFiling = AHVSoup.findAll('table')[3]
                        AHVTableLocation = AHVSoup.findAll('table')[4]
                        AHVTableContractor = AHVSoup.findAll('table')[5]
                        AHVTableVariance = AHVSoup.findAll('table')[6]

                        jobNumber = AHVTablePremises.findAll('tr')[0].findAll('td')[1].a.string
                        referenceNumber = AHVTablePremises.findAll('tr')[1].findAll('td')[1].string.replace('Reference Number: ',"")
                        findStatus = AHVTableFiling.find('td',text = 'Status:')
                        status = findStatus.findNext('td').string
                        #status = AHVTableFiling.findAll('tr')[3].findAll('td')[4].string
                        entryDate = AHVTableFiling.findAll('tr')[4].findAll('td')[5].string
                        filingType = AHVTableFiling.findAll('tr')[5].findAll('td')[3].string
                        houseNumber = AHVTableLocation.findAll('tr')[2].findAll('td')[1].string
                        streetName = AHVTableLocation.findAll('tr')[2].findAll('td')[3].string
                        borough = AHVTableLocation.findAll('tr')[3].findAll('td')[1].string
                        BIN = AHVTableLocation.findAll('tr')[3].findAll('td')[7].a.string

                        name = AHVTableContractor.findAll('tr')[2].findAll('td')[1].string
                        businessName = AHVTableContractor.findAll('tr')[3].findAll('td')[1].string
                        licenseNumber = AHVTableContractor.findAll('tr')[6].findAll('td')[3].a.string

                        residenceYes = AHVTableVariance.findAll('tr')[2].findAll('td')[1].findAll('img')
                        for images in residenceYes:
                            if images['src'] == "images/box_check.gif":
                                nearResidence = "yes"
                            else:
                                nearResidence = "no"
                        enclosedBuildingYes = AHVTableVariance.findAll('tr')[3].findAll('td')[1].findAll('img')
                        for images in enclosedBuildingYes:
                            if images['src'] == "images/box_check.gif":
                                enclosedBuilding = "yes"
                            else:
                                enclosedBuilding = "no"

                        demolitionYes = AHVTableVariance.findAll('tr')[4].findAll('td')[1].findAll('img')
                        for images in demolitionYes:
                            if images['src'] == "images/box_check.gif":
                                demolition = "yes"
                            else:
                                demolition = "no"
                        craneYes = AHVTableVariance.findAll('tr')[5].findAll('td')[1].findAll('img')
                        for images in craneYes:
                            if images['src'] == "images/box_check.gif":
                                crane = "yes"
                            else:
                                crane = "no"

                        requested = AHVTableVariance.findAll('tr')[6].findAll('td')[0].text.replace(u'\xa0', "").replace('Total Days Requested:',"").encode('utf-8')
                        approved = AHVTableVariance.findAll('tr')[7].findAll('td')[0].text.replace(u'\xa0', "").replace('Total Days Approved:',"").encode('utf-8')
                        startDay = AHVTableVariance.findAll('tr')[10].findAll('td')[0].string
                        days = AHVTableVariance.findAll('tr')[10].findAll('td')[1].string
                        try:
                            hoursFrom = AHVTableVariance.findAll('tr')[10].findAll('td')[2].string
                        except:
                            hoursFrom = 'null'
                        try:
                            hoursTo = AHVTableVariance.findAll('tr')[10].findAll('td')[3].string
                        except:
                            hoursTo = 'null'
                        findReason = AHVTableVariance.findAll('b',text = re.compile('Apply Reason:.*'))[0]
                        reason = findReason.parent.text.replace(u'\xa0', "").replace('Apply Reason:',"").strip().encode('utf-8')
                        try:
                            findApprovedReason = AHVTableVariance.findAll('b',text = re.compile('Approved:.*'))[1]
                            approvedReason = findApprovedReason.parent.text.replace(u'\xa0', "").replace('Approved:',"").strip().encode('utf-8')
                        except IndexError:
                            approvedReason = 'null'
                        try:
                            findDescription = AHVTableVariance.find('td', text = 'Description of Work:')
                            description = findDescription.findNext('td').string
                        except IndexError:
                            description = 'null'
                        f.writerow([AHVURL,jobNumber,referenceNumber,status,entryDate,filingType,houseNumber,streetName,borough,BIN,name, businessName,licenseNumber,nearResidence,enclosedBuilding,demolition,crane,requested,approved,startDay,days,hoursFrom,hoursTo,reason,approvedReason,description])

                    print 'page complete'
                    try:
                        nextPageElem = driver2.find_element_by_name('next')
                        print 'success'
                    except NoSuchElementException:
                        break
                    nextPageElem.click()
                    print 'clicked'


        driver.quit()
        driver2.quit()


if __name__ == '__main__':
    scraper = AHV_Scraper()
    scraper.scrape()
