crawlerUrl = r"https://www.idx.co.id/en-us/listed-companies/company-profiles/"

opXPath = r"//div[@id='companyTable_length']/label/select/option[@value='100']"
companyBase = r"//table[@id='companyTable']/tbody/tr"
bigTableXPath = r"%s[100]/td" % companyBase
codeXPath = r"%s/td[@class='text-center'][2]" % companyBase
nameXPath = r"%s/td/a" % companyBase
listingDateXPath = r"%s/td[4]" % companyBase

batchSaveExceptionMessage = r"Unable to save data to database."

companyIndexPath = r"data\company_index.json"
companyProfilesPath = r"data\company_profiles.json"

detailBaseXPath = r"//dd[@class='financial-report-description']"
detailCompanyNameXPath = r"%s[1]/span[@id='frName']" % detailBaseXPath
detailSecurityCodeXPath = r"%s[2]/span[@id='frSecurityCode']" % detailBaseXPath
detailAddressXPath = r"%s[3]/span[@id='frOfficeAddress']" % detailBaseXPath
detailEmailAddressXPath = r"%s[4]/span[@id='frEmail']" % detailBaseXPath
detailCountryXPath = r"Indonesia"
detailPhoneXPath = r"%s[5]/span[@id='frTelephone']" % detailBaseXPath
detailFaxXPath = r"%s[6]/span[@id='frFax']" % detailBaseXPath
detailNPWPXPath = r"%s[7]/span[@id='frNpwp']" % detailBaseXPath
detailCompanyWebsiteXPath = r"%s[8]/a[@id='frWebsite']" % detailBaseXPath
detailIPODateXPath = r"%s[9]/span[@id='frIpoDate']" % detailBaseXPath
detailBoardXPath = r"%s[10]/span[@id='frBoard']" % detailBaseXPath
detailSectorXPath = r"%s[12]/span[@id='frSector']" % detailBaseXPath
detailSubSectorXPath = r"%s[13]/span[@id='frSubSector']" % detailBaseXPath
detailRegistrarXPath = r"%s[14]/span[@id='frBAE']" % detailBaseXPath

corpSecBaseXPath = r"//table[@id='csTable']/tbody"
corpSecNameXPath = r"%s/tr[{0}]/td[1]" % corpSecBaseXPath
corpSecEmailXPath = r"%s/tr[{0}]/td[2]" % corpSecBaseXPath
corpSecPhoneXPath = r"%s/tr[{0}]/td[3]" % corpSecBaseXPath

directorBaseXPath = r"//table[@id='directorTable']/tbody"
directorNameXPath = r"%s/tr[{0}]/td[1]" % directorBaseXPath
directorPositionXPath = r"%s/tr[{0}]/td[2]" % directorBaseXPath

subsidiaryBaseXpath = r"//table[@id='subsidiaryTable']/tbody"
subsidiaryOpXPath = r"//div[@id='subsidiaryTable_length']/label/select/option[@value='100']"
subsidiaryNameXpath = r"%s/tr[{0}]/td[@class='sorting_1']" % subsidiaryBaseXpath
subsidiaryTypeXpath = r"%s/tr[{0}]/td[2]" % subsidiaryBaseXpath
subsidiaryTotalXpath = r"%s/tr[{0}]/td[3]" % subsidiaryBaseXpath
subsidiaryPercXpath = r"%s/tr[{0}]/td[4]" % subsidiaryBaseXpath
