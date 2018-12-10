from datetime import datetime
import time
import constants


class CompanyMapper(object):
    def __init__(self, browser):
        self.browser = browser

    def map(self, code, name, url, date):
        company = {
                "ticker symbol": code,
                "company name": name,
                "url": url,
                "listing_date": datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d'),
                "crawled_at": datetime.utcnow().strftime('%Y-%m-%d'),
            }
        return company

    def mapDetail(self):
        companyDetail = {
            "Company Name": self.browser.find_elements_by_xpath(constants.detailCompanyNameXPath).text,
            "Security Code": self.browser.find_elements_by_xpath(constants.detailSecurityCodeXPath).text,
            "Office address": self.browser.find_elements_by_xpath(constants.detailAddressXPath).text,
            "Email Address": self.browser.find_elements_by_xpath(constants.detailEmailAddressXPath).text,
            "Country": constants.detailCountryXPath,
            "Phone": self.mapPhones(),
            "Fax": self.mapFaxes(),
            "NPWP": self.browser.find_elements_by_xpath(constants.detailNPWPXPath).text,
            "Company Website": self.browser.find_elements_by_xpath(constants.detailCompanyWebsiteXPath).text,
            "IPO Date": self.browser.find_elements_by_xpath(constants.detailIPODateXPath).text,
            "Board": self.browser.find_elements_by_xpath(constants.detailBoardXPath).text,
            "Sector": self.browser.find_elements_by_xpath(constants.detailSectorXPath).text,
            "Sub Sector": self.browser.find_elements_by_xpath(constants.detailSubSectorXPath).text,
            "Registrar": self.browser.find_elements_by_xpath(constants.detailRegistrarXPath).text,
            "Corporate Secretary": self.mapCorporateSecretaries(),
            "Director": self.mapDirectors(),
            "Subsidiary": self.mapSubsidiaries()
        }
        return companyDetail

    def mapPhones(self):
        phones = self.browser.find_elements_by_xpath(constants.detailPhoneXPath).text
        return phones.split(',')

    def mapFaxes(self):
        faxes = self.browser.find_elements_by_xpath(constants.detailFaxXPath).text
        return faxes.split(',')

    def mapCorporateSecretaries(self):
        do = True
        corporateSecretaries = []
        index = 1
        while do:
            name = self.browser.find_elements_by_xpath(constants.corpSecNameXPath.replace("{0}", index)).text
            if name is None:
                do = False
            else:
                corporateSecretary = {
                    "name": name,
                    "email": self.browser.find_elements_by_xpath(constants.corpSecEmailXPath.replace("{0}", index)).text,
                    "phone": self.browser.find_elements_by_xpath(constants.corpSecPhoneXPath.replace("{0}", index)).text
                }
                corporateSecretaries.append(corporateSecretary)
                index = index + 1
        return corporateSecretaries

    def mapDirectors(self):
        do = True
        directors = []
        index = 1
        while do:
            name = self.browser.find_elements_by_xpath(constants.directorNameXPath.replace("{0}", index)).text
            if name is None:
                do = False
            else:
                director = {
                    "name": name,
                    "position": self.browser.find_elements_by_xpath(constants.directorPositionXPath.replace("{0}", index)).text
                }
                directors.append(director)
                index = index + 1
        # TODO: check if there's a company with more than 10 directors
        return directors

    def mapSubsidiaries(self):
        do = True
        subsidiaries = []
        index = 1
        while do:
            name = self.browser.find_elements_by_xpath(constants.subsidiaryNameXpath.replace("{0}", index)).text
            if name is None:
                do = False
            else:
                subsidiary = {
                    "name": name,
                    "type": self.browser.find_elements_by_xpath(constants.subsidiaryTypeXpath.replace("{0}", index)).text,
                    "total asset": self.browser.find_elements_by_xpath(constants.subsidiaryTotalXpath.replace("{0}", index)).text,
                    "percentage": self.browser.find_elements_by_xpath(constants.subsidiaryPercXpath.replace("{0}", index)).text
                }
                subsidiaries.append(subsidiary)

                if index == 10:
                    next = self.browser.find_element_by_id('subsidiaryTable_next')
                    if 'disabled' in next.get_attribute('class'):
                        return subsidiaries
                    next.click()
                    time.sleep(3)

                index = index + 1
        return subsidiaries
