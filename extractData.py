from os import environ
from os import mkdir
from os.path import exists
from os.path import join
from uuid import uuid4


class Extract:

    """ Tüm işlemler init başlangıç fonksiyonundan yönetilmektedir. """
    def __init__(self, fileData: list, urlAddress: str):

        desktopPath = join(join(environ['USERPROFILE']), 'Desktop')
        urlAddress = self.cleanURL(urlAddress)
        pathFolder = self.createFolder(desktopPath, urlAddress)
        fileName = uuid4()
        self.createTXT(pathFolder, fileName, fileData)

    def cleanURL(self, urlAddress: str) -> str:

        listSymbol = ["#", "<", ">", "$", "+", "'", "!", "%", "/",
                      "&", "*", "|", "{", "?", "=", ":", " ", "@"]
        cleanAddress = ""
        for i in urlAddress:
            if i not in listSymbol:
                cleanAddress += i
        return cleanAddress

    def createFolder(self, desktopPath, urlAddress: str) -> str:

        path = join(desktopPath, urlAddress)
        temp_path = path
        print("folder path : ", path)
        if exists(path) is not True:
            mkdir(path)

        else:  # TODO: bu kısım silinebilir
            print("Folder already exists")
        temp_path = temp_path + "/"
        return temp_path

    def createTXT(self, pathFolder: str, fileName: str, fileData: str) -> bool:

        txtFullPath = pathFolder + fileName + ".txt"
        try:
            with open(txtFullPath, "w", encoding="utf-8") as file:
                for i in fileData:
                    file.write(i)
                    file.write("\n")
            return True
        except IOError as err:
            print(err)
            return False
