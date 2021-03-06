
# pylint: disable=E0401,E0611
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import time
import util.constants as constants


class CompanyMapper(object):
    def __init__(self, browser):
        self.browser = browser
        self.staleElemWait = 3

    def map(self, code, name, url, date):
        """
        Maps scrapped company data to json object
        """
        company = {
            "ticker symbol": code,
            "company name": name,
            "url": url,
            "listing_date": datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d'),
            "crawled_at": datetime.utcnow().strftime('%Y-%m-%d'),
        }
        return company

    def mapDetail(self):
        """
        Maps scrapped company detail data to json object
        """
        companyDetail = {
            "Company Name": self.getElementText(constants.detailCompanyNameXPath),
            "Security Code": self.getElementText(constants.detailSecurityCodeXPath),
            "Office address": self.getElementText(constants.detailAddressXPath),
            "Email Address": self.getElementText(constants.detailEmailAddressXPath),
            "Country": constants.detailCountryXPath,
            "Phone": self.mapPhones(),
            "Fax": self.mapFaxes(),
            "NPWP": self.getElementText(constants.detailNPWPXPath),
            "Company Website": self.getElementText(constants.detailCompanyWebsiteXPath),
            "IPO Date": self.mapDate(self.getElementText(constants.detailIPODateXPath)),
            "Board": self.getElementText(constants.detailBoardXPath),
            "Sector": self.getElementText(constants.detailSectorXPath),
            "Sub Sector": self.getElementText(constants.detailSubSectorXPath),
            "Registrar": self.getElementText(constants.detailRegistrarXPath),
            "Corporate Secretary": self.mapCorporateSecretaries(),
            "Director": self.mapDirectors(),
            "Subsidiary": self.mapSubsidiaries()
        }
        return companyDetail

    def getElementText(self, xpath):
        """
        Get text from element helper
        """
        elem = self.browser.find_elements_by_xpath(xpath)
        if len(elem) > 0:
            return elem[0].text
        else:
            return ""

    def mapDate(self, date):
        """
        Map date to formatted value
        """
        if not date:
            return date
        return datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')

    def mapPhones(self):
        """
        Maps collection of phone number data to json array
        """
        phones = self.getElementText(constants.detailPhoneXPath)
        return phones.split(',')

    def mapFaxes(self):
        """
        Maps collection of fax number data to json array
        """
        faxes = self.getElementText(constants.detailFaxXPath)
        return faxes.split(',')

    def mapCorporateSecretaries(self):
        """
        Maps collection of corporate Secretary data to json array
        """
        do = True
        corporateSecretaries = []
        index = 1
        while do:
            nameElem = self.browser.find_elements_by_xpath(constants.corpSecNameXPath.format(index))
            if len(nameElem) == 0:
                do = False
            else:
                corporateSecretary = {
                    "name": nameElem[0].text,
                    "email": self.browser.find_elements_by_xpath(constants.corpSecEmailXPath.format(index))[0].text,
                    "phone": self.browser.find_elements_by_xpath(constants.corpSecPhoneXPath.format(index))[0].text
                }
                corporateSecretaries.append(corporateSecretary)
                index = index + 1
        return corporateSecretaries

    def mapDirectors(self):
        """
        Maps collection of director data to json array
        """
        do = True
        directors = []
        index = 1
        while do:
            nameElem = self.browser.find_elements_by_xpath(constants.directorNameXPath.format(index))
            if len(nameElem) == 0:
                do = False
            else:
                director = {
                    "name": nameElem[0].text,
                    "position": self.browser.find_elements_by_xpath(constants.directorPositionXPath.format(index))[0].text
                }
                directors.append(director)
                index = index + 1
        # TODO: check if there's a company with more than 10 directors
        return directors

    def mapSubsidiaries(self):
        """
        Maps collection of subsidiaries data to json array
        """
        do = True
        subsidiaries = []
        index = 1

        try:
            dropdown = self.browser.find_element_by_xpath(constants.subsidiaryOpXPath)
            dropdown.click()
            time.sleep(self.staleElemWait)
        except NoSuchElementException:
            pass

        while do:
            nameElem = self.browser.find_elements_by_xpath(constants.subsidiaryNameXpath.format(index))
            if len(nameElem) == 0:
                do = False
            else:
                subsidiary = {
                    "name": nameElem[0].text,
                    "type": self.browser.find_elements_by_xpath(constants.subsidiaryTypeXpath.format(index))[0].text,
                    "total asset": self.browser.find_elements_by_xpath(constants.subsidiaryTotalXpath.format(index))[0].text,
                    "percentage": self.browser.find_elements_by_xpath(constants.subsidiaryPercXpath.format(index))[0].text
                }
                subsidiaries.append(subsidiary)

                if index == 100:
                    nextElem = self.browser.find_element_by_id('subsidiaryTable_next')
                    if 'disabled' in nextElem.get_attribute('class'):
                        return subsidiaries
                    nextElem.click()
                    time.sleep(self.staleElemWait)
                    index = 1
                else:
                    index = index + 1
        return subsidiaries
