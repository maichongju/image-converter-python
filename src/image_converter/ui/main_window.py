import time

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QComboBox, QLabel,
                               QLineEdit, QListWidget, QFileDialog, QListWidgetItem, QMessageBox, QProgressBar)
from PySide6.QtGui import QIcon

from image_converter.utils import get_icon_path
from .file_list_item import FileListItem
from image_converter.codex import convert_images, ImageFormat
from image_converter.ui.convert_result_dialog import ConvertResultDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Converter")
        self.resize(800, 600)
        self.input_file = []
        self._output_dir = None
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

        layout_file_actions = QHBoxLayout()
        layout_input.addLayout(layout_file_actions)

        btn_add_input_files = QPushButton("Add files")
        btn_add_input_files.clicked.connect(self._btn_add_input_files_clicked)
        layout_file_actions.addWidget(btn_add_input_files)

        btn_clear_all_files = QPushButton("Clear all")
        btn_clear_all_files.clicked.connect(self._clear_all_files)
        layout_file_actions.addWidget(btn_clear_all_files)

        self.list_widget_input_files = QListWidget()
        layout_input.addWidget(self.list_widget_input_files)

        layout_output = QVBoxLayout()
        layout_top.addLayout(layout_output)
        layout_output.addWidget(QLabel("Output format:"))
        self.combo_output_format = QComboBox(main_widget)
        self.combo_output_format.addItems(ImageFormat.get_all_formats())
        self.combo_output_format.setFixedWidth(200)
        layout_output.addWidget(self.combo_output_format)

        layout_output.addWidget(QLabel("Output directory:"))
        layout_output_dir = QHBoxLayout()
        layout_output.addLayout(layout_output_dir)

        self.input_output_dir = QLineEdit()
        layout_output_dir.addWidget(self.input_output_dir)

        btn_output_dir = QPushButton()
        btn_output_dir.setIcon(QIcon(get_icon_path("folder.png")))
        btn_output_dir.clicked.connect(self._btn_set_output_dir_clicked)
        layout_output_dir.addWidget(btn_output_dir)
        layout_output.addStretch()

        self.progress_bar_convert = QProgressBar()
        layout_main.addWidget(self.progress_bar_convert)

        layout_convert = QHBoxLayout()
        layout_main.addLayout(layout_convert)

        self.btn_convert = QPushButton("Convert")
        self.btn_convert.setFixedWidth(100)
        self.btn_convert.clicked.connect(self._btn_convert_clicked)
        layout_convert.addWidget(self.btn_convert)

    def _btn_convert_clicked(self):
        if not self.input_file:
            QMessageBox.warning(self, "Error", "No files selected")
            return

        if not self._output_dir:
            QMessageBox.warning(self, "Error", "No output directory selected")
            return

        self.btn_convert.setEnabled(False)
        self.progress_bar_convert.setRange(0, len(self.input_file))
        self.progress_bar_convert.setValue(0)

        selected_format = self.combo_output_format.currentText()

        result = convert_images(self.input_file, self._output_dir, ImageFormat.from_str(selected_format),
                                self.progress_bar_convert.setValue)
        ConvertResultDialog(result, self).exec()
        self.btn_convert.setEnabled(True)

    def _btn_add_input_files_clicked(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select files", "")
        for file_name in file_names:
            self._add_file(file_name)

    def _btn_set_output_dir_clicked(self):
        output_dir = QFileDialog.getExistingDirectory(self, "Select directory", dir=self._output_dir)
        if output_dir:
            self._output_dir = output_dir
            self.input_output_dir.setText(output_dir)

    def _add_file(self, file_name):
        if file_name in self.input_file:
            print(f"File {file_name} already added")
        else:
            self.input_file.append(file_name)

            list_item = QListWidgetItem(self.list_widget_input_files)
            item = FileListItem(file_name, list_item, self._remove_file)
            list_item.setSizeHint(item.sizeHint())
            self.list_widget_input_files.addItem(list_item)
            self.list_widget_input_files.setItemWidget(list_item, item)

    def _remove_file(self, file_name: str, item: QListWidgetItem):
        self.input_file.remove(file_name)
        self.list_widget_input_files.takeItem(self.list_widget_input_files.row(item))

    def _clear_all_files(self):
        self.input_file.clear()
        self.list_widget_input_files.clear()
        self.progress_bar_convert.setValue(0)
