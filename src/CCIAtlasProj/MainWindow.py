import random

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from .controller import Controller


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Two Section Layout with Menu Bar')

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Two colored sections
        left_section = QWidget()
        left_layout = QVBoxLayout()
        self.proj_tree_view = QTreeView()
        self.proj_dir_view = QTreeView()
    
        left_layout.addWidget(self.proj_tree_view)
        left_layout.addWidget(self.proj_dir_view)
        #self.projTreeView.setStyleSheet('background-color: lightblue;')
        #self.projDirView.setStyleSheet('background-color: red;')
        left_section.setLayout(left_layout)

        stitch_dir_view = self._setup_stitch_dir_view()
        s_dir_info_view = self._setup_s_dir_info_view()
        #rightSection.setStyleSheet('background-color: lightgreen;')
        main_layout.addWidget(left_section)
        main_layout.addWidget(stitch_dir_view)
        main_layout.addWidget(s_dir_info_view)

        # Menu bar with File > Exit
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        
        self.open_proj_action = QAction('Open atlas proj', self)
        self.open_proj_action.triggered.connect(self._open_project)
        file_menu.addAction(self.open_proj_action)
        file_menu.addAction(exit_action)
        
        self.controller = None
        
    def _setup_stitch_dir_view(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        session_selet_label = QLabel("Select session to monitor:")
        self.session_combo_box = QComboBox()
        self.s_dir_view = QTreeView()
        
        main_layout.addWidget(session_selet_label)
        main_layout.addWidget(self.session_combo_box)
        main_layout.addWidget(self.s_dir_view)
        
#        self.s_dir_view.setModel(self.sessionModel)
#        self.s_dir_view.setRootIndex(QModelIndex())
        self.s_dir_view.setAlternatingRowColors(True)
        
#        self.session_combo_box.activated.connect(self.sessionActivated)
#        self.s_dir_view.clicked.connect(self.sDirSelected)
        
        return central_widget

    def _setup_s_dir_info_view(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        session_selet_label = QLabel("S_ Directory info")
        self.s_info_view = QTableView()
        self.start_stitch_btn = QPushButton("Start Stitching")

        main_layout.addWidget(session_selet_label)
        main_layout.addWidget(self.s_info_view)
        main_layout.addWidget(self.start_stitch_btn)

#        self.s_info_view.setModel(self.sDirModel)
        #self.s_dir_view.setRootIndex(QModelIndex())
        self.s_info_view.setAlternatingRowColors(True)
        self.s_info_view.horizontalHeader().show()
        return central_widget
    
    def _open_project(self):
        
        file_path, _ = QFileDialog.getOpenFileName(
        parent=self,
        caption="Select an .a5proj file",
        dir=".",  # starting directory
        filter="Atlas Project Files (*.a5proj *.xml)"
        )

        if file_path and self.controller:
            self.controller.load_file(file_path)
            self.proj_tree_view.setModel(self.controller.get_atlas_model())
            
    def connect_controller(self, controller: Controller):
        self.controller = controller
        #self.proj_tree_view.setModel(self.controller.get_atlas_model())
        
        #self.open_proj_action.triggered.connect(self.controller.load_file)
        
    # @QtCore.Slot()
    # def magic(self):
    #     self.text.setText(random.choice(self.hello))
