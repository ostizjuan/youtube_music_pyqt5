import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout
from qframelesswindow import FramelessWindow, TitleBar
from PyQt5.Qt import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QPixmap

from PyQt5 import QtCore, QtNetwork, QtWidgets

class UniqueApplication(QtWidgets.QApplication):
    anotherInstance = QtCore.pyqtSignal()
    def isUnique(self):
        socket = QtNetwork.QLocalSocket()
        socket.connectToServer('Youtube Music')
        return not socket.state()

    def startListener(self):
        self.listener = QtNetwork.QLocalServer(self)
        self.listener.setSocketOptions(self.listener.WorldAccessOption)
        self.listener.newConnection.connect(self.anotherInstance)
        self.listener.listen('Youtube Music')

class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):

        super().__init__(parent)
        self.title = QLabel('Youtube Music', self)
        self.title.setStyleSheet("QLabel{font: 13px 'Century Gothic'; font-weight: bold ;margin: 10px; color:white;}")
        self.title.adjustSize()
        
        self.icon = QLabel(self)
        self.icon.setPixmap(QPixmap("icono.ico"))
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
        self.setMinimumSize(int(sizes.width()/1.9), int(sizes.height()/1.7))

        self.myLay = QVBoxLayout(self)
        self.myLay.setContentsMargins(0, 32, 0, 0)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://music.youtube.com"))
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


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # run app
    app = UniqueApplication(sys.argv)
    if not app.isUnique():
        pass
    else:
        app.startListener()
        sizes = app.primaryScreen().size()
        demo = Window(sizes)
        demo.show()
        sys.exit(app.exec_())