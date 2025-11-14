import sys

from PySide6.QtWidgets import QApplication

from CCIAtlasProj.controller import Controller
from CCIAtlasProj.MainWindow import MainWidget

#from .cli import app

if __name__ == "__main__":

    # app = QGuiApplication(sys.argv)
    # engine = QQmlApplicationEngine()
    # base = Path(__file__).resolve().parent
    # engine.addImportPath(base / "qml")
    # #engine.addImportPath(sys.path[0])
    # #engine.loadFromModule("main", "Main")
    # engine.load(base / "qml" / "MainWindow.qml")
    # if not engine.rootObjects():
    #     sys.exit(-1)
    # exit_code = app.exec()
    # del engine
    # sys.exit(exit_code)
    controller = Controller()

    app = QApplication(sys.argv)
    win = MainWidget()
    win.connect_controller(controller)
    win.show()
    exit_code = app.exec()
    sys.exit(exit_code)
