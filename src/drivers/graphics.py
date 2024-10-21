# make pretty graphs and a GUI
import sys
from PyQt5.QtWidgets import QApplication, QWidget

# Create the main application
app = QApplication(sys.argv)

# Create a window widget
window = QWidget()
window.setWindowTitle('Flight Simulation GUI')
window.setGeometry(100, 100, 800, 600)  # x, y, width, height

# Show the window
window.show()

# Start the application's event loop
sys.exit(app.exec_())
