from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QListWidget
from PySide6.QtGui import QIcon

from image_converter.utils import get_icon_path

SUPPORTED_FORMATS = ['JPEG', 'PNG']


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Converter")
        self.resize(800, 600)
        self.input_file = []
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout_main = QVBoxLayout()
        main_widget.setLayout(layout_main)

        layout_top = QHBoxLayout()
        layout_main.addLayout(layout_top)

        layout_input = QVBoxLayout()
        layout_top.addLayout(layout_input)

        layout_input.addWidget(QLabel("Source files:"))
        btn_add_input_files = QPushButton("Add files")
        layout_input.addWidget(btn_add_input_files)
        list_widget_input_files = QListWidget()
        layout_input.addWidget(list_widget_input_files)

        layout_output = QVBoxLayout()
        layout_top.addLayout(layout_output)
        layout_output.addWidget(QLabel("Output format:"))
        combo_output_format = QComboBox(main_widget)
        combo_output_format.addItems(SUPPORTED_FORMATS)
        combo_output_format.setFixedWidth(200)
        layout_output.addWidget(combo_output_format)

        layout_output.addWidget(QLabel("Output directory:"))
        layout_output_dir = QHBoxLayout()
        layout_output.addLayout(layout_output_dir)

        input_output_dir = QLineEdit()
        layout_output_dir.addWidget(input_output_dir)

        btn_output_dir = QPushButton()
        btn_output_dir.setIcon(QIcon(get_icon_path("folder.png")))
        layout_output_dir.addWidget(btn_output_dir)
        layout_output.addStretch()

        layout_convert = QHBoxLayout()
        layout_main.addLayout(layout_convert)

        btn_convert = QPushButton("Convert")
        btn_convert.setFixedWidth(100)
        btn_convert.clicked.connect(self._btn_convert_clicked)
        layout_convert.addWidget(btn_convert)

    def _btn_convert_clicked(self):
        pass

    def _btn_add_input_files_clicked(self):
        pass
