from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Scraper:


    """ Tüm işlevler init başlangıç fonksiyonundan yönetilmektedir. """
    def __init__(self, chrome_driverPath: str, locatorName: str):
        self.browser = Chrome(chrome_driverPath)

        """ Dictionary yapısını kullanarak çoklu bir koşul işlemi gerçekleştirildi. """
        """ Kullanıcı hangi konum belirleyiciyi kullanacaksa diğer işlevler bu duruma göre ayarlandı. """
        dictLocator = {"XPath": By.XPATH, "Id": By.ID}
        self.selectedLocator = dictLocator[locatorName]

        """ Bu fonksiyon, açılan tarayıcı penceresini maksimum boyuta ayarlar. """
    def maxWindow(self):
        self.browser.maximize_window()

        """ Bu fonksiyon, tarayıcıda bir sayfanın tamamen yüklenmesini bekletir. """
    def waitLoaded(self):
        self.browser.implicitly_wait(7)

        """ Bu fonksiyon, kullanıcı tarafından verilen url adresinin tarayıcı üzerinde açılmasını sağlar. """
    def openURL(self, urlAddress: str):
        self.browser.get(urlAddress)

        """ Bu fonksiyon, web sayfasındaki bir entry'nin içerisine veri gönderebilmeyi sağlar. """
    def forEntry(self, location: str, data: str):
        entry = self.browser.find_element(by=self.selectedLocator, value=location)
        WebDriverWait(self.browser, 2)
        entry.send_keys(data)

        """ Bu fonksiyon, web sayfasındaki bir buton'a tıklayabilmemizi sağlar. """
    def forButton(self, location: str) -> bool:
        button = self.browser.find_element(by=self.selectedLocator, value=location)
        button.click()
        return True

        """ Bu fonksiyon, içeriğinde metin barındıran konumlardan veri almayı sağlar. """
    def forText(self, location: str) -> str:
        data = self.browser.find_element(by=self.selectedLocator, value=location).text
        return data

        """ Bu fonksiyon, web sayfasındaki tüm içeriklerin yüklenmesini sağlamak için
         scroll barı sayfanın altına getirir. """
    def scrollToEnd(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
