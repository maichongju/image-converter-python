from PySide6.QtWidgets import QDialog, QLabel, QTextEdit, QVBoxLayout, QPushButton
from image_converter.codex import ConvertResult


class ConvertResultDialog(QDialog):
    def __init__(self, result: ConvertResult, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conversion result")
        self.resize(400, 300)
        self._result = result
        self.setup_ui()

    def setup_ui(self):
        layout_main = QVBoxLayout()
        self.setLayout(layout_main)

        layout_main.addWidget(QLabel("Conversion result:"))
        layout_main.addWidget(QLabel(f"Total: {self._result.total} Success: {self._result.success} Failed: {self._result.failed}"))

        if self._result.errors:
            text_errors = QTextEdit()
            text_errors.setReadOnly(True)
            text_errors.setPlainText('\n'.join(self._result.errors))
            layout_main.addWidget(text_errors)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        layout_main.addWidget(btn_close)
        layout_main.addStretch()

