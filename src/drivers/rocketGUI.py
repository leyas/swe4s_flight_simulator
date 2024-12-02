from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import matplotlib.pyplot as plt
import json
from rocketDrawing import RocketDrawing  # Custom drawing class
from aeroCalcs import AeroCalcs  # Aero calculations


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)  # Adjusted for graph space

        # Main Page
        self.mainPage = QtWidgets.QWidget(MainWindow)
        self.mainPage.setObjectName("mainPage")

        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self.mainPage)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1180, 780))
        self.tabWidget.setObjectName("tabWidget")

        # Simulation Tab
        self.Simulation = QtWidgets.QWidget()
        self.Simulation.setObjectName("Simulation")

        # Layout for Simulation Tab
        self.sim_layout = QtWidgets.QGridLayout(self.Simulation)

        # Left Panel: Input Widgets
        self.input_group = QtWidgets.QGroupBox("Rocket Inputs")
        self.input_layout = QtWidgets.QGridLayout(self.input_group)

        # Input Widgets
        self.af_d_label = QtWidgets.QLabel("Airframe Diameter (in):")
        self.af_d_input = QtWidgets.QDoubleSpinBox()
        self.af_d_input.setDecimals(1)
        self.af_d_input.setMaximum(100.0)

        self.af_l_label = QtWidgets.QLabel("Airframe Length (in):")
        self.af_l_input = QtWidgets.QDoubleSpinBox()
        self.af_l_input.setDecimals(1)
        self.af_l_input.setMaximum(500.0)

        self.nc_l_label = QtWidgets.QLabel("Nose Cone Length (in):")
        self.nc_l_input = QtWidgets.QDoubleSpinBox()
        self.nc_l_input.setDecimals(1)
        self.nc_l_input.setMaximum(50.0)

        self.nc_shape_label = QtWidgets.QLabel("Nose Cone Shape:")
        self.nc_list = QtWidgets.QListWidget()
        for item in ["Tangent Ogive", "Elliptic", "Conic"]:
            self.nc_list.addItem(item)

        self.input_layout.addWidget(self.af_d_label, 0, 0)
        self.input_layout.addWidget(self.af_d_input, 0, 1)
        self.input_layout.addWidget(self.af_l_label, 1, 0)
        self.input_layout.addWidget(self.af_l_input, 1, 1)
        self.input_layout.addWidget(self.nc_l_label, 2, 0)
        self.input_layout.addWidget(self.nc_l_input, 2, 1)
        self.input_layout.addWidget(self.nc_shape_label, 3, 0)
        self.input_layout.addWidget(self.nc_list, 3, 1)

        self.sim_layout.addWidget(self.input_group, 0, 0)

         # Fins Group Box
        self.fins_group = QtWidgets.QGroupBox("Fins Customization")
        self.fins_layout = QtWidgets.QGridLayout(self.fins_group)

        # Sweep Angle
        self.sweep_angle_label = QtWidgets.QLabel("Sweep Angle (deg):")
        self.sweep_angle_input = QtWidgets.QDoubleSpinBox()
        self.sweep_angle_input.setDecimals(1)
        self.sweep_angle_input.setMaximum(90.0)
        self.sweep_angle_input.setSingleStep(1.0)

        # Tip Chord
        self.tip_chord_label = QtWidgets.QLabel("Tip Chord (in):")
        self.tip_chord_input = QtWidgets.QDoubleSpinBox()
        self.tip_chord_input.setDecimals(1)
        self.tip_chord_input.setMaximum(50.0)
        self.tip_chord_input.setSingleStep(0.5)

        # Semi-Span
        self.semi_span_label = QtWidgets.QLabel("Semi-Span (in):")
        self.semi_span_input = QtWidgets.QDoubleSpinBox()
        self.semi_span_input.setDecimals(1)
        self.semi_span_input.setMaximum(50.0)
        self.semi_span_input.setSingleStep(0.5)

        # Root Chord
        self.root_chord_label = QtWidgets.QLabel("Root Chord (in):")
        self.root_chord_input = QtWidgets.QDoubleSpinBox()
        self.root_chord_input.setDecimals(1)
        self.root_chord_input.setMaximum(50.0)
        self.root_chord_input.setSingleStep(0.5)

        # Add Widgets to Fins Layout
        self.fins_layout.addWidget(self.sweep_angle_label, 0, 0)
        self.fins_layout.addWidget(self.sweep_angle_input, 0, 1)
        self.fins_layout.addWidget(self.tip_chord_label, 1, 0)
        self.fins_layout.addWidget(self.tip_chord_input, 1, 1)
        self.fins_layout.addWidget(self.semi_span_label, 2, 0)
        self.fins_layout.addWidget(self.semi_span_input, 2, 1)
        self.fins_layout.addWidget(self.root_chord_label, 3, 0)
        self.fins_layout.addWidget(self.root_chord_input, 3, 1)

        # Add Fins Group Box to Layout
        self.sim_layout.addWidget(self.fins_group, 1, 0)

        # Right Panel: Graph and Button
        self.graph_group = QtWidgets.QGroupBox("Rocket Design")
        self.graph_layout = QtWidgets.QVBoxLayout(self.graph_group)

        # Matplotlib Figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.Simulation)

        # Display Rocket Button
        self.display_button = QtWidgets.QPushButton("Display Rocket Design")
        self.display_button.clicked.connect(self.display_rocket_design)

        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)
        self.graph_layout.addWidget(self.display_button)

        self.sim_layout.addWidget(self.graph_group, 0, 1)

        # Add Simulation Tab to Tab Widget
        self.tabWidget.addTab(self.Simulation, "Simulation Tab")

        # Set Central Widget
        MainWindow.setCentralWidget(self.mainPage)

        self.retranslateUi(MainWindow)
        self.connect_signals()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rocket Design UI"))

    def connect_signals(self):
        """Connect widget value changes to JSON update methods."""
        self.af_d_input.valueChanged.connect(self.update_af_diameter)
        self.af_l_input.valueChanged.connect(self.update_af_length)
        self.nc_l_input.valueChanged.connect(self.update_nc_length)
        self.nc_list.itemClicked.connect(self.update_nc_shape)

        # Fins connections
        self.sweep_angle_input.valueChanged.connect(self.update_sweep_angle)
        self.tip_chord_input.valueChanged.connect(self.update_tip_chord)
        self.semi_span_input.valueChanged.connect(self.update_semi_span)
        self.root_chord_input.valueChanged.connect(self.update_root_chord)

    def update_json(self, section, key, value):
        """Update the JSON file with the specified key-value pair."""
        json_file = "../config/rocket_specs.json"
        try:
            with open(json_file, "r") as file:
                data = json.load(file)

            if section in data and key in data[section]:
                data[section][key] = value

            with open(json_file, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"An error occurred: {e}")

    def update_af_diameter(self, value):
        self.update_json("air_frame", "diameter", value)

    def update_af_length(self, value):
        self.update_json("air_frame", "length", value)

    def update_nc_length(self, value):
        self.update_json("nose_cone", "length", value)

    def update_nc_shape(self, item):
        shape = item.text().lower().replace(" ", "_")
        self.update_json("nose_cone", "shape", shape)

    def update_sweep_angle(self, value):
        self.update_json("fins", "sweep_angle", value)

    def update_tip_chord(self, value):
        self.update_json("fins", "tip_chord", value)

    def update_semi_span(self, value):
        self.update_json("fins", "semi_span", value)

    def update_root_chord(self, value):
        self.update_json("fins", "root_chord", value)

    def display_rocket_design(self):
        """
        Display the rocket design in the embedded Matplotlib graph.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Load the rocket specs JSON
        rocket_specs_file = "../config/rocket_specs.json"
        with open(rocket_specs_file, "r") as file:
            rocket_specs = json.load(file)

        # Create an instance of AeroCalcs to calculate CG and CP
        aero_calcs = AeroCalcs(rocket_specs, material="fiberglass", motor="K")
        cg = aero_calcs.calculate_center_of_gravity()
        cp = aero_calcs.calculate_center_of_pressure()

        # Draw the rocket using RocketDrawing
        rocket_drawing = RocketDrawing(rocket_specs, cg, cp)
        rocket_drawing.plot_rocket(ax)  # Pass the axis for plotting

        # Update the canvas in the GUI
        self.canvas.draw()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
