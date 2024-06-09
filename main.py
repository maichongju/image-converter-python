import os
import sys

import qdarktheme
from PySide6.QtWidgets import QApplication

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_converter.ui.main_window import MainWindow

qdarktheme.enable_hi_dpi()
app = QApplication(sys.argv)
qdarktheme.setup_theme(theme='light')

window = MainWindow()
window.show()
app.exec()
