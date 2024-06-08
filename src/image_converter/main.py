from PySide6.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow
import qdarktheme


qdarktheme.enable_hi_dpi()
app = QApplication(sys.argv)
qdarktheme.setup_theme(theme='light')

window = MainWindow()
window.show()
app.exec()
