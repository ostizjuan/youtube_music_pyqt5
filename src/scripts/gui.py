from os import path, getcwd

from PyQt5.QtCore import Qt, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from qframelesswindow import FramelessWindow, TitleBar
from PyQt5.Qt import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile, QWebEnginePage


class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):

        super().__init__(parent)
        self.title = QLabel('Youtube Music', self)
        self.title.setStyleSheet(
            "QLabel{font: 13px 'Century Gothic'; font-weight: bold ;margin: 10px; color:white;}")
        self.title.adjustSize()

        self.icon = QLabel(self)
        self.icon.setPixmap(
            QPixmap(path.join(getcwd(), 'src', 'icono.ico')))
        self.icon.setScaledContents(True)
        self.icon.setFixedSize(30, 30)
        self.icon.setStyleSheet("QLabel{margin: 3px;}")
        self.hBoxLayout.insertWidget(0, self.icon, 100, Qt.AlignLeft)
        self.hBoxLayout.insertWidget(1, self.title, 100, Qt.AlignLeft)
        self.hBoxLayout.setContentsMargins(3, 0, 0, 0)

        # customize the style of title bar button
        self.minBtn.updateStyle({
            "normal": {
                'color': (255, 255, 255)
            }
        })

        self.maxBtn.updateStyle({
            "normal": {
                'color': (255, 255, 255)
            }
        })

        self.closeBtn.updateStyle({
            "normal": {
                "icon": ':/framelesswindow/close_white.svg',
                'color': (255, 255, 255)
            }
        })


class Window(FramelessWindow):

    def __init__(self, sizes=(800, 600), parent=None):
        # change the default title bar if you like
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.setWindowTitle("Youtube Music")
        self.setStyleSheet("background:#212121;")
        self.titleBar.raise_()

        # define the settings
        self.settings = QSettings('ostizjuan', 'Youtube Music')
        # if don't have the size, the window will be the size of the screen / 1.9 and / 1.7
        self.resize(self.settings.value("size", QSize(
            int(sizes.width()/1.9), int(sizes.height()/1.7))))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        self.last_url = self.settings.value('url', 'https://music.youtube.com')
        # it can't be smaller that size of the screen / 1.9 and / 1.7
        self.setMinimumSize(int(sizes.width()/1.9), int(sizes.height()/1.7))
        self.myLay = QVBoxLayout(self)
        self.myLay.setContentsMargins(0, 32, 0, 0)

        # define the browser
        self.profile = QWebEngineProfile("YT", self)
        self.webpage = QWebEnginePage(self.profile, self)
        self.browser = QWebEngineView(self)
        self.browser.setPage(self.webpage)
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.setUrl(QUrl(self.last_url))

        # adding style and disabling 'view source' and 'save page' options
        self.browser.setStyleSheet('''
            QMenu {
                background: #282828;
                color: white;
            }
            QMenu::item:selected {
                background: lightGray;
            }
        ''')
        self.browser.page().action(QWebEnginePage.ViewSource).setVisible(False)
        self.browser.page().action(QWebEnginePage.SavePage).setVisible(False)

        self.myLay.addWidget(self)
        self.myLay.addWidget(self.browser)
        self.setLayout(self.myLay)

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.move(
            self.width() // 2 - length // 2,
            self.height() // 2 - length // 2
        )

    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue('url', self.browser.url().toString())
        e.accept()
