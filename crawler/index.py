# pylint: disable=E0401,E0611
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import util.constants as constants
from util.companyMapper import CompanyMapper
import time
import json
import os
import multiprocessing
from multiprocessing import Pool


class SeleniumCrawler(object):

    def __init__(self):
        self.browser = webdriver.Chrome(constants.chromeDriverPath,
                                        chrome_options=SeleniumCrawler.getOptions())
        self.browser.get(constants.crawlerUrl)
        time.sleep(1)
        self.companyMapper = CompanyMapper(self.browser)
        self.companyUrls = []

    def run(self):
        """
        Runs the SeleniumCrawler, first scrapes companies then scrapes details for all companies 
        """
        try:
            cores = multiprocessing.cpu_count()
            dropdown = self.browser.find_element_by_xpath(constants.opXPath)
            dropdown.click()
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((
                    By.XPATH, constants.bigTableXPath)))

            items = self.crawlCompanies([])
            self.browser.quit()
            SeleniumCrawler.saveJsonDocument(constants.companyIndexPath, items)
            items = []

            SeleniumCrawler.fileWriter(constants.companyProfilesPath, '[')

            p = Pool(processes=cores)
            p.map(SeleniumCrawler.crawlCompanyDetails, self.companyUrls)
            
            SeleniumCrawler.removeCharFromFile(constants.companyProfilesPath)
            SeleniumCrawler.fileWriter(constants.companyProfilesPath, ']')

        except Exception as ex:
            print(ex)
            self.browser.quit()

    def crawlCompanies(self, items):
        """
        Scrapes company data
        """
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

        nextElem = self.browser.find_element_by_id('companyTable_next')
        if 'disabled' in nextElem.get_attribute('class'):
            return items
        nextElem.click()
        time.sleep(3)

        return self.crawlCompanies(items)

    @staticmethod
    def getOptions():
        """
        Headless browser driver options
        """
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        return options

    @staticmethod
    def crawlCompanyDetails(companyUrl: str):
        """
        Scrapes details for all companies 
        """
        print("Loading [%s]." % companyUrl)
        driver = webdriver.Chrome(constants.chromeDriverPath, chrome_options=SeleniumCrawler.getOptions())
        driver.get(companyUrl)
        time.sleep(1)
        companyMapper = CompanyMapper(driver)
        companyDetail = companyMapper.mapDetail()
        driver.quit()
        SeleniumCrawler.saveJsonDocument(constants.companyProfilesPath, companyDetail, True, 'a+')

    @staticmethod
    def saveJsonDocument(path: str, data, isMultiPro = False, m: str = 'w+'):
        """
        Converts data to json before saving to file
        """
        d = json.dumps(data, indent=4, sort_keys=True)
        if isMultiPro:
            d = d + ','
        SeleniumCrawler.fileWriter(path, d, m)

    @staticmethod
    def getFilePath(path: str):
        """
        Gets absolute file path for given filename
        """
        basepath = os.path.dirname(__file__)
        abs_file_path = os.path.abspath(os.path.join(basepath, "..", path))
        return abs_file_path

    @staticmethod
    def fileWriter(path: str, data, m = 'a+'):
        """
        Writes file to disk
        """
        abs_file_path = SeleniumCrawler.getFilePath(path)
        f = open(abs_file_path, m)
        f.write(data)

    @staticmethod
    def removeCharFromFile(filename: str):
        """
        Removes last char from file
        """
        with open(filename, 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()


if __name__ == '__main__':
    a = SeleniumCrawler()
    a.run()
