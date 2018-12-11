from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants
from companyMapper import CompanyMapper
import time
from datetime import datetime
import json
import os
from multiprocessing import Pool


class SeleniumCrawler(object):

    def __init__(self):
        self.browser = webdriver.Chrome(constants.chromeDriverPath,
                                        chrome_options=SeleniumCrawler.getOptions())
        self.browser.get(constants.crawlerUrl)
        time.sleep(1)
        self.companyMapper = CompanyMapper(self.browser)
        self.companyUrls = []

    @staticmethod
    def getOptions():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        return options

    def run(self):
        try:
            dropdown = self.browser.find_element_by_xpath(constants.opXPath)
            dropdown.click()
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((
                    By.XPATH, constants.bigTableXPath)))

            items = self.crawlCompanies([])
            self.browser.quit()
            SeleniumCrawler.saveJsonDocument(constants.companyIndexPath, items)
            items = []

            p = Pool(processes=6)
            p.map(SeleniumCrawler.crawlCompanyDetails, self.companyUrls)

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
            print("%s added." % companyNames[i].text)
            self.companyUrls.append(companyNames[i].get_attribute('href'))
            items.append(company)

        next = self.browser.find_element_by_id('companyTable_next')
        if 'disabled' in next.get_attribute('class'):
            return items
        next.click()
        time.sleep(3)

        return self.crawlCompanies(items)

    @staticmethod
    def crawlCompanyDetails(companyUrl):
        print("Loading [%s]." % companyUrl)
        driver = webdriver.Chrome(constants.chromeDriverPath, chrome_options=SeleniumCrawler.getOptions())
        driver.get(companyUrl)
        time.sleep(1)
        companyMapper = CompanyMapper(driver)
        companyDetail = companyMapper.mapDetail()
        driver.quit()
        SeleniumCrawler.saveJsonDocument(constants.companyProfilesPath, companyDetail, 'a+')

    @staticmethod
    def saveJsonDocument(path, data, m='w'):
        basepath = os.path.dirname(__file__)
        abs_file_path = os.path.abspath(os.path.join(basepath, "..", path))
        with open(abs_file_path, m) as outfile:
            json.dump(data, outfile)

if __name__ == '__main__':
    a = SeleniumCrawler()
    a.run()
