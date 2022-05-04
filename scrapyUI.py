from sys import argv, exit
from time import sleep

from PyQt5.QtCore import Qt, QDir, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QMenuBar, QMenu, QLineEdit, QPushButton, \
    QFileDialog, QMessageBox, QVBoxLayout, QComboBox, QLabel, QFormLayout, QGroupBox, QScrollArea

""" Diğer modüller dahil edildi. """
import extractData as fileOperations
import scrapy


class MainWindow(QWidget):

    def __init__(self):
        self.iconAdd = "add.png"
        self.iconBack = "backicon.png"
        self.iconFile = "fileicon.jpg"
        self.iconNext = "next.png"
        self.iconOutput = "output.png"

        self.styleButton = ("QPushButton"
                            "{" "background-color: #2ecc71;"
                            "color:white;"
                            "font-size : 16px;"
                            "padding:10px;"
                            "border-radius:10%;"
                            "}"
                            "QPushButton::hover"
                            "{"
                            "background-color : lightgreen;"
                            "}")

        self.styleQLineEdit = ("padding:7px;"
                               "font-size:15px;"
                               "border: 2px solid gray;"
                               "border-radius: 10px;"
                               "background-color:white;"
                               "width:400")

        app = QApplication(argv)

        super().__init__()
        self.mainLayout = QHBoxLayout()

        self.setWindowTitle("Scrapping UI")
        self.setFixedSize(1000, 600)

        menu = QMenuBar()
        quitMenu = QMenu("Güvenli çıkış")
        quitMenu.addAction("Güvenli çıkış", lambda: QApplication.quit())
        menu.addMenu(quitMenu)

        self.page_1()

        self.mainLayout.setMenuBar(menu)
        self.setLayout(self.mainLayout)
        self.show()

        exit(app.exec())

    def deleteLayoutsWidget(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteLayoutsWidget(item.layout())

    def createEntry(self, placeholder: str, fixedWidth: int) -> object:
        entry = QLineEdit()
        entry.setStyleSheet(self.styleQLineEdit)
        entry.setPlaceholderText(placeholder)
        entry.setFixedWidth(fixedWidth)
        return entry

    def createButton(self, title: str, fixedWidth: int, toolTip: str) -> object:
        button = QPushButton(title)
        button.setStyleSheet(self.styleButton)
        button.setFixedWidth(fixedWidth)
        button.setToolTip(toolTip)
        return button

    def manageEntry(self, placeholder: str, locatorName: str):

        if placeholder == "Entry için " + locatorName + " girin":
            entry = self.createEntry("Entry için " + locatorName + " girin", 500)
            entryInfo = self.createEntry("Entry için veri girin", 250)
            self.tempFormLayout.addRow(entry)
            self.tempFormLayout.addRow(entryInfo)
            self.listEntryWidget.append([entry, entryInfo])
            self.tempFormLayout.setAlignment(Qt.AlignTop)
            self.groupBox.setLayout(self.tempFormLayout)
            self.scrollArea.setWidget(self.groupBox)
            self.rightLayout.addWidget(self.scrollArea)
            self.rightLayout.addWidget(self.btnGetData, alignment=Qt.AlignCenter)

        else:
            entry = self.createEntry(placeholder, 500)
            self.tempFormLayout.addRow(entry)
            self.listEntryWidget.append(entry)

            self.tempFormLayout.setAlignment(Qt.AlignTop)
            self.groupBox.setLayout(self.tempFormLayout)
            self.scrollArea.setWidget(self.groupBox)
            self.rightLayout.addWidget(self.scrollArea)
            self.rightLayout.addWidget(self.btnGetData, alignment=Qt.AlignCenter)

    def getFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath(), '*.exe')
        self.pathDriver = ""
        if fileName != "":
            self.pathDriver = fileName
            QMessageBox.information(self, "Bilgilendirme", "Driver eklenmiştir...")
        else:
            QMessageBox.information(self, "Bilgilendirme", "Driver eklenmedi!")

    def page_1(self):

        self.deleteLayoutsWidget(self.mainLayout)

        rightLayout = QVBoxLayout()

        driverSelect = QPushButton("Driver ekle")
        driverSelect.setIcon(QIcon(self.iconAdd))
        driverSelect.setIconSize(QSize(30, 30))
        driverSelect.setStyleSheet(self.styleButton)
        driverSelect.setFixedWidth(150)
        driverSelect.clicked.connect(lambda: self.getFileName())

        pathURL = self.createEntry("Sitenin Url adresini girin", 350)

        btnNext = self.createButton("İleri", 100, "Diğer sayfaya geçer")
        btnNext.setIcon(QIcon(self.iconNext))
        btnNext.setIconSize(QSize(30, 30))
        btnNext.clicked.connect(lambda: self.page_2(pathURL.text(), selectLocator.currentText()))

        selectLocator = QComboBox()
        selectLocator.setToolTip("Konum belirleyici seçin")
        selectLocator.addItems(["Konum belirleyici seçin", "XPath", "Id"])
        selectLocator.setStyleSheet(
            "background:snow;""color:lightgreen;""font:bold 12px;""border: 1px solid gray;"
            "border-radius: 3px;""padding: 1px 18px 1px 3px;""min-width: 6em;""max-width:10em;""padding:5px;"
        )

        [rightLayout.addWidget(i, alignment=Qt.AlignCenter) for i in
         [pathURL, selectLocator, driverSelect, btnNext]]
        rightLayout.setAlignment(Qt.AlignTop)
        rightLayout.setSpacing(40)
        rightLayout.setContentsMargins(10, 50, 10, 100)
        self.mainLayout.addLayout(rightLayout)

    def page_2(self, pathURL: str, locatorName: str):

        self.pathURL = pathURL
        self.listEntryWidget = []
        self.listData = []
        self.locator = locatorName

        self.deleteLayoutsWidget(self.mainLayout)

        leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        labelInfo = QLabel("Bot oluşturmak istediğiniz sitede veriye ulaşırken gerçekleştirilen tüm işlemleri \n"
                           "konum belirleyicileri kullanarak tasarlayın ve ardından çalıştırın")
        labelInfo.setStyleSheet("color:lightgreen;""font-size:17px;")

        self.tempFormLayout = QFormLayout()
        self.groupBox = QGroupBox("")
        self.groupBox.setContentsMargins(100, 1, 1, 1)
        self.scrollArea = QScrollArea()
        # self.scrollArea.setGeometry(0,0,400,500)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setEnabled(True)

        addEntryforEntry = self.createButton("Entry için giriş ekle", 200, "")
        addEntryforEntry.setIcon(QIcon(self.iconAdd))
        addEntryforEntry.setIconSize(QSize(30, 30))
        addEntryforEntry.clicked.connect(
            lambda: self.manageEntry("Entry için " + locatorName + " girin", locatorName))

        addEntryforButton = self.createButton("Buton için giriş ekle", 200, "")
        addEntryforButton.clicked.connect(
            lambda: self.manageEntry("Buton için " + locatorName + " girin", locatorName))
        addEntryforButton.setIcon(QIcon(self.iconAdd))
        addEntryforButton.setIconSize(QSize(30, 30))

        addEntryforText = self.createButton("Text için giriş ekle", 200, "")
        addEntryforText.clicked.connect(
            lambda: self.manageEntry("Veri için " + locatorName + " girin", locatorName))
        addEntryforText.setIcon(QIcon(self.iconAdd))
        addEntryforText.setIconSize(QSize(30, 30))

        self.btnGetData = self.createButton("Çalıştır", 250, " Veri çıktısını masaüstünde oluşturur")
        self.btnGetData.clicked.connect(lambda: self.getData())
        self.btnGetData.setIcon(QIcon(self.iconOutput))
        self.btnGetData.setIconSize(QSize(30, 30))

        goBackButton = QPushButton()
        goBackButton.setStyleSheet(
            "color:blue;""font-size:30px;""background_color:gray;")  # TODO : bu butona geri dönüş ikonu eklenecek
        goBackButton.setContentsMargins(0, 0, 0, 0)
        goBackButton.setFixedWidth(100)
        goBackButton.setIcon(QIcon(self.iconBack))
        goBackButton.setIconSize(QSize(30, 30))
        goBackButton.clicked.connect(lambda: self.page_1())

        self.rightLayout.addWidget(labelInfo, alignment=Qt.AlignCenter)
        self.rightLayout.setAlignment(Qt.AlignTop)
        [leftLayout.addWidget(i, alignment=Qt.AlignCenter) for i in
         [goBackButton, addEntryforEntry, addEntryforButton, addEntryforText]]

        leftLayout.setSpacing(100)
        self.mainLayout.addLayout(leftLayout, 1)
        self.mainLayout.addLayout(self.rightLayout, 4)
        self.mainLayout.setAlignment(Qt.AlignTop)

    def createFile(self):
        fileOperations.Extract(fileData=self.listData, urlAddress=self.pathURL)

    

    def getData(self):

        sc = scrapy.Scraper(self.pathDriver, self.locator)
        sc.openURL(self.pathURL)  # verilen url'i tarayıcıda açar
        sc.maxWindow()
        sc.waitLoaded()  # sayfanın yüklenmesini bekler.
        sc.scrollToEnd(len(self.listEntryWidget))
        for i in range(len(self.listEntryWidget)):
            sleep(2)

            """ Entry'lerin hangi widget için oluşturulduğunu kontrol etmek için bu sorgular yapıldı."""
            """ İlgili widget için yapılacak işlemler scrappingClass modülünden yararlanılarak gerçekleştirildi."""

            if type(self.listEntryWidget[i]) == type(list()):
                sc.forEntry(self.listEntryWidget[i][0].text(), self.listEntryWidget[i][1].text())
                continue

            elif "Buton" in self.listEntryWidget[i].placeholderText():
                sc.forButton(self.listEntryWidget[i].text())
                continue

            elif "Veri" in self.listEntryWidget[i].placeholderText():
                data = sc.forText(self.listEntryWidget[i].text())
                self.listData.append(data)


        if len(self.listData) != 0:
            self.createFile()
            QMessageBox.information(self, "Bilgilendirme", "Veri başarıyla çıkarıldı, masaüstünüzü kontrol edin!")
        else:
            QMessageBox.information(self, "Veri bulunamadı", "Lütfen konum belirleyicileri kontrol edin!")


window = MainWindow()
