#import random

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

from cci_atlas_proj.atlas_geometry import AtlasRectangle
from cci_atlas_proj.controller import Controller


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Two Section Layout with Menu Bar")

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
        # self.projTreeView.setStyleSheet('background-color: lightblue;')
        # self.projDirView.setStyleSheet('background-color: red;')
        left_section.setLayout(left_layout)

        new_reqion_view = self._setup_new_region_view()

        # stitch_dir_view = self._setup_stitch_dir_view()
        # s_dir_info_view = self._setup_s_dir_info_view()
        # # rightSection.setStyleSheet('background-color: lightgreen;')
        main_layout.addWidget(left_section)
        main_layout.addWidget(new_reqion_view)
        # main_layout.addWidget(stitch_dir_view)
        # main_layout.addWidget(s_dir_info_view)

        # Menu bar with File > Exit
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        self.open_proj_action = QAction("Open atlas proj", self)
        self.open_proj_action.triggered.connect(self._open_project)
        
        self.save_proj_action = QAction("Save atlas proj", self)
        self.save_proj_action.triggered.connect(self._save_project)
        
        file_menu.addAction(self.open_proj_action)
        file_menu.addAction(self.save_proj_action)
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

    def _setup_new_region_view(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        region_label = QLabel("Create New Region")
        protocol_label = QLabel("select Protocol:")
        self.protocol_combo_box = QComboBox()
        
        self.new_region_btn = QPushButton("New Region")
        self.new_region_btn.clicked.connect(self.create_new_region)
        self.new_region_btn.setEnabled(False)

        main_layout.addWidget(region_label)
        main_layout.addWidget(protocol_label)
        main_layout.addWidget(self.protocol_combo_box)
        main_layout.addWidget(self.new_region_btn)

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
        # self.s_dir_view.setRootIndex(QModelIndex())
        self.s_info_view.setAlternatingRowColors(True)
        self.s_info_view.horizontalHeader().show()
        return central_widget

    def create_new_region(self):
        if self.controller:
            doc = self.controller.get_atlas_model().get_document()
            geometry = AtlasRectangle(x=1000, y=2000, w=1000, h=1000, dom_doc=doc)
            prot_data = self.protocol_combo_box.currentData()
            prot_uid = prot_data[1]
            self.controller.create_new_region(geometry, prot_uid)

    def _open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select an .a5proj file",
            dir=".",  # starting directory
            filter="Atlas Project Files (*.a5proj *.xml)",
        )

        if file_path and self.controller:
            self.controller.load_file(file_path)
            atlas_model = self.controller.get_atlas_model()
            self.proj_tree_view.setModel(atlas_model)
            self.proj_dir_view.setModel(atlas_model)
            self.proj_dir_view.setRootIndex(atlas_model.get_region_set_index())
            self.new_region_btn.setEnabled(True)

    def _save_project(self):
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Select an .a5proj file",
            dir=".",  # starting directory
            filter="Atlas Project Files (*.a5proj *.xml)",
        )

        if file_path and self.controller:
            self.controller.save_dom_to_file(file_path)

    def _populate_protocol_combo_box(self):
        if self.controller:
            protocols_model = self.controller.get_protocols_model()
            if protocols_model:
                protos = protocols_model.get_protocols()
                for proto in protos:
                    self.protocol_combo_box.addItem(proto[0], proto)
                    
    def connect_controller(self, controller: Controller):
        self.controller = controller
        self._populate_protocol_combo_box()
        # self.proj_tree_view.setModel(self.controller.get_atlas_model())

        # self.open_proj_action.triggered.connect(self.controller.load_file)

    # @QtCore.Slot()
    # def magic(self):
    #     self.text.setText(random.choice(self.hello))
