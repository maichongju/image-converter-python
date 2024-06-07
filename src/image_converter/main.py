from PySide6.QtWidgets import QApplication
import sys
from ui.main_window import MainWindow

# sys.argv += ['-platform', 'windows:darkmode=1']
app = QApplication(sys.argv)
app.setStyleSheet('')
window = MainWindow()
window.show()
app.exec()
