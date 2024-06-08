from PySide6.QtWidgets import QHBoxLayout, QWidget, QLabel, QPushButton, QListWidgetItem
import typing


class FileListItem(QWidget):
    def __init__(self, file_path: str, item: QListWidgetItem, delete_cb: typing.Callable, parent=None):
        super().__init__(parent)
        self._delete_cb = delete_cb
        self._file_path = file_path
        self._item = item
        self._setup_ui(file_path)

    def _setup_ui(self, path: str):
        layout_main = QHBoxLayout()
        self.setLayout(layout_main)

        btn_delete = QPushButton("X")
        btn_delete.clicked.connect(self._btn_delete_clicked)
        btn_delete.setFixedWidth(20)
        layout_main.addWidget(btn_delete)
        layout_main.addWidget(QLabel(path))

    def _btn_delete_clicked(self):
        self._delete_cb(self._file_path, self._item)
