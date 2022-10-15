from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtNetwork


class UniqueApplication(QApplication):
    """Application that allows only one instance to run"""
    anotherInstance = QtCore.pyqtSignal()

    def __init__(self, argv):
        super().__init__(argv)

    def isUnique(self):
        socket = QtNetwork.QLocalSocket()
        socket.connectToServer('Youtube Music')
        return not socket.state()

    def startListener(self):
        self.listener = QtNetwork.QLocalServer(self)
        self.listener.setSocketOptions(self.listener.WorldAccessOption)
        self.listener.newConnection.connect(self.anotherInstance)
        self.listener.listen('Youtube Music')
