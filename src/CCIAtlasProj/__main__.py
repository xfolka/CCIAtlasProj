import sys
from pathlib import Path

#import MainWindow
from PySide6 import QtCore, QtGui, QtWidgets
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


#from .cli import app

if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    base = Path(__file__).resolve().parent
    engine.addImportPath(base / "qml")
    #engine.addImportPath(sys.path[0])
    #engine.loadFromModule("main", "Main")
    engine.load(base / "qml" / "MainWindow.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)

