from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants
from companyMapper import CompanyMapper
import time
from datetime import datetime
import json
import os


class SeleniumCrawler(object):

    def __init__(self):
        self.browser = webdriver.Chrome(constants.chromeDriverPath)
        self.browser.get(constants.crawlerUrl)
        # self.repository = Repo(constants.dbUri)
        self.companyMapper = CompanyMapper(self.browser)
        self.companyUrls = []

    def run(self):
        try:
            dropdown = self.browser.find_element_by_xpath(constants.opXPath)
            dropdown.click()
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, constants.bigTableXPath)))

            items = self.crawlCompanies([])
            self.saveJsonDocument(constants.companyIndexPath, items)
            items = []

            items = self.crawlCompanyDetails([])
            self.saveJsonDocument(constants.companyProfilesPath, items)
            items = []
        except Exception as ex:
            print(ex)

        self.browser.quit()

    def crawlCompanies(self, items):
        codes = self.browser.find_elements_by_xpath(constants.codeXPath)
        companyNames = self.browser.find_elements_by_xpath(constants.nameXPath)
        dates = self.browser.find_elements_by_xpath(
            constants.listingDateXPath)

        for i in range(len(codes)):
            company = self.companyMapper.map(codes[i].text,
                                             companyNames[i].text,
                                             companyNames[i].get_attribute('href'),
                                             dates[i].text)
            self.companyUrls.append(companyNames[i].get_attribute('href'))
            items.append(company)

        next = self.browser.find_element_by_id('companyTable_next')
        if 'disabled' in next.get_attribute('class'):
            return items
        next.click()
        time.sleep(5)

        return self.crawlCompanies(items)

    def crawlCompanyDetails(self, companyDetails):
        for companyUrl in self.companyUrls:
            self.browser.get(companyUrl)
            companyDetail = self.companyMapper.mapDetail()
            companyDetails.append(companyDetail)
        return companyDetails

    def saveJsonDocument(self, path, data):
        basepath = os.path.dirname(__file__)
        abs_file_path = os.path.abspath(os.path.join(basepath, "..",path))
        with open(abs_file_path, 'w') as outfile:
            json.dump(data, outfile)

if __name__ == '__main__':
    a = SeleniumCrawler()
    a.run()
