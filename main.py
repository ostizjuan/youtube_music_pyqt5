import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from src.scripts.unique import UniqueApplication
from src.scripts.gui import Window


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
        try:
            app.startListener()
            sizes = app.primaryScreen().size()
            window = Window(app, sizes)
            window.show()
            sys.exit(app.exec_())
        except Exception as e:
            print(e)
