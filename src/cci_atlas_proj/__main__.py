import sys
from importlib.resources import files

from PySide6.QtWidgets import QApplication

from cci_atlas_proj import data
from cci_atlas_proj.controller import Controller
from cci_atlas_proj.main_window import MainWidget

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
    win.load_project_file(files(data) / "empty-project.a5proj")
    win.show()
    exit_code = app.exec()
    sys.exit(exit_code)
