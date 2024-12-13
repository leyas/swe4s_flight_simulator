from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from PyQt5.QtGui import QPixmap, QFont
import matplotlib.pyplot as plt
import numpy as np
import json
import os

from rocketDrawing import RocketDrawing  # Custom drawing class
from aeroCalcs import AeroCalcs  # Aero calculations
from physCalcs import PhysCalcs

class Ui_MainWindow(object):
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        # Get screen dimensions
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set MainWindow size as a percentage of the screen resolution
        MainWindow.resize(int(screen_width * 0.8), int(screen_height * 0.8))  # 80% of screen width and height

        # Main Page
        self.mainPage = QtWidgets.QWidget(MainWindow)
        self.mainPage.setObjectName("mainPage")

        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self.mainPage)
        # Set QTabWidget size relative to the screen size
        self.tabWidget.setGeometry(QtCore.QRect(
                int(screen_width * 0.01),  # X position (1% of screen width)
                int(screen_height * 0.01),  # Y position (1% of screen height)
                int(screen_width * 0.78),  # Width (78% of screen width)
                int(screen_height * 0.78)  # Height (78% of screen height)
            ))
        self.tabWidget.setObjectName("tabWidget")

        # Simulation Tab
        self.Simulation = QtWidgets.QWidget()
        self.Simulation.setObjectName("Simulation")

        # Create a scrollable area for the Simulation Tab
        self.simulation_scroll = QtWidgets.QScrollArea(self.Simulation)
        self.simulation_scroll.setWidgetResizable(True)

        # Create a container widget for the Simulation Tab content
        self.simulation_container = QtWidgets.QWidget()
        self.sim_layout = QtWidgets.QGridLayout(self.simulation_container)

        # Layout for Simulation Tab
        #self.sim_layout = QtWidgets.QGridLayout(self.Simulation)

        # Create Airframe Group Box
        self.airframe_group = QtWidgets.QGroupBox("Airframe Customization")
        self.airframe_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        airframe_font = self.airframe_group.font()
        airframe_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.airframe_group.setFont(airframe_font)
        self.airframe_layout = QtWidgets.QGridLayout(self.airframe_group)

        # Airframe labels and inputs
        label_font = QFont()
        label_font.setPointSize(int(screen_height * 0.005))  # 0.5% of screen height for labels
        self.af_d_label = QtWidgets.QLabel("Airframe Diameter (in):")
        self.af_d_label.setFont(label_font)
        self.af_d_input = QtWidgets.QDoubleSpinBox()
        self.af_d_input.setDecimals(1)
        self.af_d_input.setMaximum(100.0)
        self.af_l_label = QtWidgets.QLabel("Airframe Length (in):")
        self.af_l_label.setFont(label_font)
        self.af_l_input = QtWidgets.QDoubleSpinBox()
        self.af_l_input.setDecimals(1)
        self.af_l_input.setMaximum(500.0)

        self.airframe_layout.addWidget(self.af_d_label, 0, 0)
        self.airframe_layout.addWidget(self.af_d_input, 0, 1)
        self.airframe_layout.addWidget(self.af_l_label, 1, 0)
        self.airframe_layout.addWidget(self.af_l_input, 1, 1)
        self.sim_layout.addWidget(self.airframe_group, 0, 0)

        # Create Nose Cone Group Box
        self.nose_group = QtWidgets.QGroupBox("Nose Cone Customization")
        self.nose_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        nose_font = self.nose_group.font()
        nose_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.nose_group.setFont(nose_font)
        self.nose_layout = QtWidgets.QGridLayout(self.nose_group)

        # Nose Cone labels and inputs
        self.nc_l_label = QtWidgets.QLabel("Nose Cone Length (in):")
        self.nc_l_label.setFont(label_font)  # Same label font as Airframe
        self.nc_l_input = QtWidgets.QDoubleSpinBox()
        self.nc_l_input.setDecimals(1)
        self.nc_l_input.setMaximum(50.0)
        self.nc_shape_label = QtWidgets.QLabel("Nose Cone Shape:")
        self.nc_shape_label.setFont(label_font)
        self.nc_list = QtWidgets.QListWidget()
        for item in ["Tangent Ogive", "Elliptic", "Conic"]:
            self.nc_list.addItem(item)

        self.nose_layout.addWidget(self.nc_l_label, 0, 0)
        self.nose_layout.addWidget(self.nc_l_input, 0, 1)
        self.nose_layout.addWidget(self.nc_shape_label, 1, 0)
        self.nose_layout.addWidget(self.nc_list, 1, 1)
        self.sim_layout.addWidget(self.nose_group, 1, 0)
        
        self.sim_layout.addWidget(self.nose_group, 1, 0)

        # Create Fins Group Box
        self.fins_group = QtWidgets.QGroupBox("Fins Customization")
        self.fins_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        fins_font = self.fins_group.font()
        fins_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.fins_group.setFont(fins_font)
        self.fins_layout = QtWidgets.QGridLayout(self.fins_group)

        # Fins labels and inputs
        label_font = QFont()
        label_font.setPointSize(int(screen_height * 0.005))  # 0.5% of screen height for labels

        # Sweep Angle
        self.sweep_angle_label = QtWidgets.QLabel("Sweep Angle (deg):")
        self.sweep_angle_label.setFont(label_font)
        self.sweep_angle_input = QtWidgets.QDoubleSpinBox()
        self.sweep_angle_input.setDecimals(1)
        self.sweep_angle_input.setMaximum(90.0)
        self.sweep_angle_input.setSingleStep(1.0)

        # Tip Chord
        self.tip_chord_label = QtWidgets.QLabel("Tip Chord (in):")
        self.tip_chord_label.setFont(label_font)
        self.tip_chord_input = QtWidgets.QDoubleSpinBox()
        self.tip_chord_input.setDecimals(1)
        self.tip_chord_input.setMaximum(50.0)
        self.tip_chord_input.setSingleStep(0.5)

        # Semi-Span
        self.semi_span_label = QtWidgets.QLabel("Semi-Span (in):")
        self.semi_span_label.setFont(label_font)
        self.semi_span_input = QtWidgets.QDoubleSpinBox()
        self.semi_span_input.setDecimals(1)
        self.semi_span_input.setMaximum(50.0)
        self.semi_span_input.setSingleStep(0.5)

        # Root Chord
        self.root_chord_label = QtWidgets.QLabel("Root Chord (in):")
        self.root_chord_label.setFont(label_font)
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
        self.sim_layout.addWidget(self.fins_group, 2, 0, 2, 1)  # Adjust row span for better spacing

       # Create Material Group Box
        self.material_group = QtWidgets.QGroupBox("Material Customization")
        self.material_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        material_font = self.material_group.font()
        material_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.material_group.setFont(material_font)
        self.material_layout = QtWidgets.QGridLayout(self.material_group)

        # Material labels and inputs
        label_font = QFont()
        label_font.setPointSize(int(screen_height * 0.005))  # 0.5% of screen height for labels

        # Material Label
        self.material_label = QtWidgets.QLabel("Materials:")
        self.material_label.setFont(label_font)
        self.material_list = QtWidgets.QListWidget()
        for item in ["Fiberglass", "Blue Tube"]:
            self.material_list.addItem(item)

        # Add Widgets to Material Layout
        self.material_layout.addWidget(self.material_label, 0, 0)
        self.material_layout.addWidget(self.material_list, 0, 1)

        # Add Material Group Box to Layout
        self.sim_layout.addWidget(self.material_group, 4, 0)


        # Create Motor Group Box
        self.motor_group = QtWidgets.QGroupBox("Motor Selection")
        self.motor_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        motor_font = self.motor_group.font()
        motor_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.motor_group.setFont(motor_font)
        self.motor_layout = QtWidgets.QGridLayout(self.motor_group)

        # Motor labels and inputs
        label_font = QFont()
        label_font.setPointSize(int(screen_height * 0.005))  # 0.5% of screen height for labels

        # Motor Label
        self.motor_label = QtWidgets.QLabel("Available motors:")
        self.motor_label.setFont(label_font)
        self.motor_list = QtWidgets.QListWidget()
        for item in ["G", "H", "I", "J", "K", "L"]:
            self.motor_list.addItem(item)

        # Add Widgets to Motor Layout
        self.motor_layout.addWidget(self.motor_label, 0, 0)
        self.motor_layout.addWidget(self.motor_list, 0, 1)

        # Add Motor Group Box to Layout
        self.sim_layout.addWidget(self.motor_group, 4, 1)

       # Create Parachute Group Box
        self.parachute_group = QtWidgets.QGroupBox("Parachute Customization")
        self.parachute_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        parachute_font = self.parachute_group.font()
        parachute_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.parachute_group.setFont(parachute_font)
        self.parachute_layout = QtWidgets.QGridLayout(self.parachute_group)

        # Parachute labels and inputs
        label_font = QFont()
        label_font.setPointSize(int(screen_height * 0.005))  # 0.5% of screen height for labels

        # Parachute Label
        self.parachute_label = QtWidgets.QLabel("Parachute Sizes:")
        self.parachute_label.setFont(label_font)
        self.parachute_list = QtWidgets.QListWidget()
        for item in ["Small (15 inch)", "Medium (28 inch)", "Large (42 inch)"]:
            self.parachute_list.addItem(item)

        # Add Widgets to Parachute Layout
        self.parachute_layout.addWidget(self.parachute_label, 0, 0)
        self.parachute_layout.addWidget(self.parachute_list, 0, 1)

        # Add Parachute Group Box to Layout
        self.sim_layout.addWidget(self.parachute_group, 6, 0, 1, 2)


        ## Right Panel: Graph and Button for Rocket Design##################33333
        # Create Rocket Design Group Box
        self.graph_group1 = QtWidgets.QGroupBox("Rocket Design")
        self.graph_group1.setStyleSheet("QGroupBox { font-weight: bold; }")
        design_font = self.graph_group1.font()
        design_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for title
        self.graph_group1.setFont(design_font)
        self.graph_layout1 = QtWidgets.QVBoxLayout(self.graph_group1)

        # Matplotlib Figure for Rocket Design
        self.design_figure = plt.figure()
        self.design_canvas = FigureCanvas(self.design_figure)
        self.design_toolbar = NavigationToolbar(self.design_canvas, self.Simulation)
        self.design_toolbar.setFixedHeight(25)

        # Display Rocket Button
        self.display_button = QtWidgets.QPushButton("Display Rocket Design")
        self.display_button.setFont(label_font)  # Match font style
        self.display_button.clicked.connect(self.display_rocket_design)

        # Add Widgets to Rocket Design Layout
        self.graph_layout1.addWidget(self.design_toolbar)
        self.graph_layout1.addWidget(self.design_canvas)
        self.graph_layout1.addWidget(self.display_button)

        # Add Rocket Design Group to Layout
        self.sim_layout.addWidget(self.graph_group1,0, 1, 1, 1)  # Spans 2 rows

        # Create Rocket Flight Path Group Box
        self.graph_group2 = QtWidgets.QGroupBox("Rocket Flight Path")
        self.graph_group2.setStyleSheet("QGroupBox { font-weight: bold; }")
        flight_font = self.graph_group2.font()
        flight_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for title
        self.graph_group2.setFont(flight_font)
        self.graph_layout2 = QtWidgets.QVBoxLayout(self.graph_group2)

        # Matplotlib Figure for Rocket Flight Path
        self.flight_figure = plt.figure()
        self.flight_canvas = FigureCanvas(self.flight_figure)
        self.flight_toolbar = NavigationToolbar(self.flight_canvas, self.Simulation)
        self.flight_toolbar.setFixedHeight(25)

        # Plot Button
        self.plot_button = QtWidgets.QPushButton("Plot Z Position")
        self.plot_button.setFont(label_font)  # Match font style
        self.plot_button.clicked.connect(self.plot_y_position)

        # Add Widgets to Rocket Flight Path Layout
        self.graph_layout2.addWidget(self.flight_toolbar)
        self.graph_layout2.addWidget(self.flight_canvas)
        self.graph_layout2.addWidget(self.plot_button)

        # Add Rocket Flight Path Group to Layout
        self.sim_layout.addWidget(self.graph_group2, 1, 1, 2, 1)

        # Add Simulation Tab to Tab Widget
        self.tabWidget.addTab(self.Simulation, "Simulation Tab")

        ##### Information Tab #############################################################
        self.Information = QtWidgets.QWidget()
        self.Information.setObjectName("Information")

        # Layout for Information Tab
        #self.info_layout = QtWidgets.QGridLayout(self.Information)

        # Add information Tab to Tab Widget
        self.tabWidget.addTab(self.Information, "Information Tab")

        self.setup_info_tab()

        # Set Central Widget
        MainWindow.setCentralWidget(self.mainPage)

        self.retranslateUi(MainWindow)
        self.connect_signals()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
"""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        # Get screen dimensions
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set MainWindow size as a percentage of the screen resolution
        MainWindow.resize(int(screen_width * 0.9), int(screen_height * 0.9))  # 80% of screen width and height

        # Main Page
        self.mainPage = QtWidgets.QWidget(MainWindow)
        self.mainPage.setObjectName("mainPage")

        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self.mainPage)
        # Set QTabWidget size relative to the screen size
        self.tabWidget.setGeometry(QtCore.QRect(
                int(screen_width * 0.01),  # X position (1% of screen width)
                int(screen_height * 0.01),  # Y position (1% of screen height)
                int(screen_width * 0.87),  # Width (87% of screen width)
                int(screen_height * 0.87)  # Height (87% of screen height)
            ))
        self.tabWidget.setObjectName("tabWidget")

        # Simulation Tab
        self.Simulation = QtWidgets.QWidget()
        self.Simulation.setObjectName("Simulation")

        # Layout for Simulation Tab
        self.sim_layout = QtWidgets.QGridLayout(self.Simulation)

        # Create Airframe Group Box
        self.airframe_group = QtWidgets.QGroupBox("Airframe Customization")
        self.airframe_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        airframe_font = self.airframe_group.font()
        airframe_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.airframe_group.setFont(airframe_font)
        self.airframe_layout = QtWidgets.QGridLayout(self.airframe_group)

        # Airframe labels and inputs
        label_font = QFont()
        label_font.setPointSize(int(screen_height * 0.005))  # 0.5% of screen height for labels
        self.af_d_label = QtWidgets.QLabel("Airframe Diameter (in):")
        self.af_d_label.setFont(label_font)
        self.af_d_input = QtWidgets.QDoubleSpinBox()
        self.af_d_input.setDecimals(1)
        self.af_d_input.setMaximum(100.0)
        self.af_l_label = QtWidgets.QLabel("Airframe Length (in):")
        self.af_l_label.setFont(label_font)
        self.af_l_input = QtWidgets.QDoubleSpinBox()
        self.af_l_input.setDecimals(1)
        self.af_l_input.setMaximum(500.0)

        self.airframe_layout.addWidget(self.af_d_label, 0, 0)
        self.airframe_layout.addWidget(self.af_d_input, 0, 1)
        self.airframe_layout.addWidget(self.af_l_label, 1, 0)
        self.airframe_layout.addWidget(self.af_l_input, 1, 1)
        self.sim_layout.addWidget(self.airframe_group, 0, 0)

        # Create Nose Cone Group Box
        self.nose_group = QtWidgets.QGroupBox("Nose Cone Customization")
        self.nose_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        nose_font = self.nose_group.font()
        nose_font.setPointSize(int(screen_height * 0.006))  # 0.6% of screen height for group box title
        self.nose_group.setFont(nose_font)
        self.nose_layout = QtWidgets.QGridLayout(self.nose_group)

        # Nose Cone labels and inputs
        self.nc_l_label = QtWidgets.QLabel("Nose Cone Length (in):")
        self.nc_l_label.setFont(label_font)  # Same label font as Airframe
        self.nc_l_input = QtWidgets.QDoubleSpinBox()
        self.nc_l_input.setDecimals(1)
        self.nc_l_input.setMaximum(50.0)
        self.nc_shape_label = QtWidgets.QLabel("Nose Cone Shape:")
        self.nc_shape_label.setFont(label_font)
        self.nc_list = QtWidgets.QListWidget()
        for item in ["Tangent Ogive", "Elliptic", "Conic"]:
            self.nc_list.addItem(item)

        self.nose_layout.addWidget(self.nc_l_label, 0, 0)
        self.nose_layout.addWidget(self.nc_l_input, 0, 1)
        self.nose_layout.addWidget(self.nc_shape_label, 1, 0)
        self.nose_layout.addWidget(self.nc_list, 1, 1)
        self.sim_layout.addWidget(self.nose_group, 1, 0)
        self.sim_layout.addWidget(self.nose_group, 1, 0)

        # Fins Group Box
        self.fins_group = QtWidgets.QGroupBox("Fins Customization")
        self.fins_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        fin_font = self.fins_group.font()
        fin_font.setPointSize(int(screen_height*0.006))
        self.fins_group.setFont(fin_font)
        self.fins_layout = QtWidgets.QGridLayout(self.fins_group)

        # Sweep Angle
        self.sweep_angle_label = QtWidgets.QLabel("Sweep Angle (deg):")
        self.sweep_angle_label.setFont(label_font)
        self.sweep_angle_input = QtWidgets.QDoubleSpinBox()
        self.sweep_angle_input.setDecimals(1)
        self.sweep_angle_input.setMaximum(90.0)
        self.sweep_angle_input.setSingleStep(1.0)

        # Tip Chord
        self.tip_chord_label = QtWidgets.QLabel("Tip Chord (in):")
        self.tip_chord_label.setFont(label_font)
        self.tip_chord_input = QtWidgets.QDoubleSpinBox()
        self.tip_chord_input.setDecimals(1)
        self.tip_chord_input.setMaximum(50.0)
        self.tip_chord_input.setSingleStep(0.5)

        # Semi-Span
        self.semi_span_label = QtWidgets.QLabel("Semi-Span (in):")
        self.semi_span_label.setFont(label_font)
        self.semi_span_input = QtWidgets.QDoubleSpinBox()
        self.semi_span_input.setDecimals(1)
        self.semi_span_input.setMaximum(50.0)
        self.semi_span_input.setSingleStep(0.5)

        # Root Chord
        self.root_chord_label = QtWidgets.QLabel("Root Chord (in):")
        self.root_chord_label.setFont(label_font)
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
        self.sim_layout.addWidget(self.fins_group, 2, 0)

        # Body Material
        self.material_group = QtWidgets.QGroupBox("Material Customization")
        self.material_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        material_font = self.material_group.font()
        material_font.setPointSize(int(screen_height*0.006))
        self.material_group.setFont(material_font)
        self.material_layout = QtWidgets.QGridLayout(self.material_group)

        self.material_label = QtWidgets.QLabel("Materials:")
        self.material_label.setFont(label_font)
        self.material_list = QtWidgets.QListWidget()
        for item in ["Fiberglass", "Blue Tube"]:
            self.material_list.addItem(item)

        self.material_layout.addWidget(self.material_label, 2, 0)
        self.material_layout.addWidget(self.material_list, 2, 1)

        self.sim_layout.addWidget(self.material_group, 3, 0)


        # Motors
        self.motor_group = QtWidgets.QGroupBox("Motor Selection")
        self.motor_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        motor_font = self.motor_group.font()
        motor_font.setPointSize(int(screen_height*0.006))
        self.motor_group.setFont(motor_font)
        self.motor_layout = QtWidgets.QGridLayout(self.motor_group)

        self.motor_label = QtWidgets.QLabel("Available motors:")
        self.motor_label.setFont(label_font)
        self.motor_list = QtWidgets.QListWidget()
        for item in ["G", "H", "I", "J", "K", "L"]:
            self.motor_list.addItem(item)

        self.motor_layout.addWidget(self.motor_label, 2, 0)
        self.motor_layout.addWidget(self.motor_list, 2, 1)

        self.sim_layout.addWidget(self.motor_group, 4, 1)

        # Parachute size
        self.parachute_group = QtWidgets.QGroupBox("Parachute Customization")
        self.parachute_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        parachute_font = self.parachute_group.font()
        parachute_font.setPointSize(int(screen_height*0.006))
        self.parachute_group.setFont(parachute_font)
        self.parachute_layout = QtWidgets.QGridLayout(self.parachute_group)

        self.parachute_label = QtWidgets.QLabel("Materials:")
        self.parachute_label.setFont(label_font)
        self.parachute_list = QtWidgets.QListWidget()
        for item in ["Small (15 inch)", "Medium (28 inch)", "Larger (42 inch)"]:
            self.parachute_list.addItem(item)

        self.parachute_layout.addWidget(self.parachute_label, 4, 0)
        self.parachute_layout.addWidget(self.parachute_list, 4, 1)

        self.sim_layout.addWidget(self.parachute_group, 4, 0)

        ## Right Panel: Graph and Button for Rocket Design
        self.graph_group1 = QtWidgets.QGroupBox("Rocket Design")
        self.graph_group1.setStyleSheet("QGroupBox { font-weight: bold; }")
        graph_font = self.graph_group1.font()
        graph_font.setPointSize(int(screen_height*0.006))
        self.graph_group1.setFont(graph_font)
        self.graph_layout1 = QtWidgets.QVBoxLayout(self.graph_group1)

        # Matplotlib Figure
        self.design_figure = plt.figure()
        self.design_canvas = FigureCanvas(self.design_figure)
        self.design_toolbar = NavigationToolbar(self.design_canvas, self.Simulation)
        self.design_toolbar.setFixedHeight(25)

        # Display Rocket Button
        self.display_button = QtWidgets.QPushButton("Display Rocket Design")
        self.display_button.clicked.connect(self.display_rocket_design)
        
        self.graph_layout1.addWidget(self.design_toolbar)
        self.graph_layout1.addWidget(self.design_canvas)
        self.graph_layout1.addWidget(self.display_button)

        self.sim_layout.addWidget(self.graph_group1, 0, 1, 2, 1)

        # Right Panel: Graph and Button for Plot
        self.graph_group2 = QtWidgets.QGroupBox("Rocket Flight Path")
        self.graph_group2.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.graph_group2.setFont(graph_font)
        self.graph_layout2 = QtWidgets.QVBoxLayout(self.graph_group2)

        # Matplotlib Figure
        self.flight_figure = plt.figure()
        self.flight_canvas = FigureCanvas(self.flight_figure)
        self.flight_toolbar = NavigationToolbar(self.flight_canvas, self.Simulation)
        self.flight_toolbar.setFixedHeight(25)

        # Plot Y Position Button
        self.plot_button = QtWidgets.QPushButton("Plot Z Position")
        self.plot_button.clicked.connect(self.plot_y_position)

        self.graph_layout2.addWidget(self.flight_toolbar)
        self.graph_layout2.addWidget(self.flight_canvas)
        self.graph_layout2.addWidget(self.plot_button)

        self.sim_layout.addWidget(self.graph_group2, 2, 1, 2, 1)

        # Add Simulation Tab to Tab Widget
        self.tabWidget.addTab(self.Simulation, "Simulation Tab")

        ##### Information Tab ##################
        self.Information = QtWidgets.QWidget()
        self.Information.setObjectName("Information")

        # Layout for Information Tab
        #self.info_layout = QtWidgets.QGridLayout(self.Information)

        # Add information Tab to Tab Widget
        self.tabWidget.addTab(self.Information, "Information Tab")

        self.setup_info_tab()

        # Set Central Widget
        MainWindow.setCentralWidget(self.mainPage)

        self.retranslateUi(MainWindow)
        self.connect_signals()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        runs the gui
        """
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
        self.design_figure.clear()
        ax = self.design_figure.add_subplot(111)

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
        self.design_canvas.draw()

    def plot_y_position(self):
        """Plot Y position with gradient in the embedded Matplotlib graph."""
        self.flight_figure.clear()
        ax = self.flight_figure.add_subplot(111)

        # # Create an instance of PhysCalcs and simulate
        # phys_calcs = PhysCalcs("../config/rocket_specs.json", material="fiberglass", motor="K")
        # try:
        #     time, x, y, vx, vy = phys_calcs.simulate()
        #     velocity = np.sqrt(vx**2 + vy**2)

        #     # Normalize velocities for color gradient
        #     norm = plt.Normalize(velocity.min(), velocity.max())
        #     points = np.array([time, y]).T.reshape(-1, 1, 2)
        #     segments = np.concatenate([points[:-1], points[1:]], axis=1)

        #     # Create LineCollection for gradient
        #     from matplotlib.collections import LineCollection
        #     lc = LineCollection(segments, cmap="viridis", norm=norm)
        #     lc.set_array(velocity)
        #     lc.set_linewidth(2)
        #     ax.add_collection(lc)

        #     # Add colorbar and set labels
        #     ax.set_title("Rocket Y-Position Over Time with Velocity Gradient")
        #     ax.set_xlabel("Time (s)")
        #     ax.set_ylabel("Y Position (m)")
        #     ax.grid()
        #     cbar = self.flight_figure.colorbar(lc, ax=ax)
        #     cbar.set_label("Velocity (m/s)")

        #     ax.set_xlim(time.min(), time.max())
        #     ax.set_ylim(y.min() - 10, y.max() + 10)

        #     # Update the canvas in the GUI
        #     self.flight_canvas.draw()

        # except Exception as e:
        #     print(f"Error in plot_y_position: {e}")

        # Create an instance of PhysCalcs and simulate
        # phys_calcs = PhysCalcs("../config/rocket_specs.json", material="fiberglass", motor="K")
        # try:
        #     time, x, y, vx, vy = phys_calcs.simulate()
        #     norm = plt.Normalize(velocity.min(), velocity.max())

        #     if y.any() > 0:
        #         velocity = (np.sqrt(vx**2 + vy**2)) * 3.2804
        #         norm = velocity
        #     else:
        #         velocity = 0

        #     # Normalize velocities for color gradient
            
        #     points = np.array([time, y]).T.reshape(-1, 1, 2)
        #     segments = np.concatenate([points[:-1], points[1:]], axis=1)

        #     # Create LineCollection for gradient
        #     from matplotlib.collections import LineCollection
        #     lc = LineCollection(segments, cmap="viridis", norm=norm)
        #     lc.set_array(velocity)
        #     lc.set_linewidth(2)
        #     ax.add_collection(lc)

        #     # Add colorbar and set labels
        #     ax.set_title("Rocket Y-Position Over Time with Velocity Gradient")
        #     ax.set_xlabel("Time (s)")
        #     ax.set_ylabel("Y Position (in.)")
        #     ax.grid()
        #     cbar = self.flight_figure.colorbar(lc, ax=ax)
        #     cbar.set_label("Velocity (ft/s)")

        #     ax.set_xlim(time.min(), time.max())
        #     ax.set_ylim(y.min() - 10, y.max() + 10)

        #     # Update the canvas in the GUI
        #     self.flight_canvas.draw()
        # except Exception as e:
        #     print(f"Error in plot_y_position: {e}")
            
        # Create an instance of PhysCalcs and simulate
        phys_calcs = PhysCalcs("../config/rocket_specs.json", material="fiberglass", motor="K")
        try:
            # Simulate and get data
            time, x, y, vx, vy = phys_calcs.simulate()

            # Compute velocity magnitude
            velocity = np.sqrt(vx**2 + vy**2)

            # Normalize velocities for color gradient
            norm = plt.Normalize(velocity.min(), velocity.max())
            points = np.array([time, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            # Create LineCollection for gradient
            from matplotlib.collections import LineCollection
            lc = LineCollection(segments, cmap="viridis", norm=norm)
            lc.set_array(velocity)
            lc.set_linewidth(2)
            ax.add_collection(lc)

            # Add colorbar and set labels
            ax.set_title("Rocket Y-Position Over Time with Velocity Gradient")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Z Position (ft)")
            ax.grid()
            cbar = self.flight_figure.colorbar(lc, ax=ax)
            cbar.set_label("Velocity (ft/s)")

            # Set plot limits
            ax.set_xlim(time.min(), time.max())
            ax.set_ylim(y.min() - 10, y.max() + 10)

            # Update the canvas in the GUI
            self.flight_canvas.draw()
        except Exception as e:
            print(f"Error in plot_y_position: {e}")

    def setup_info_tab(self):
        """ Sets up info tab based on json file"""
        json_file = "C:\\Users\\lshaw\\Desktop\\swe4s\\project\\swe4s_flight_simulator\\src\\config\\info_content.json"
        pictures_folder = "C:\\Users\\lshaw\\Desktop\\swe4s\\project\\swe4s_flight_simulator\\src\\pictures"
        
        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea(self.Information)
        scroll_area.setWidgetResizable(True)
        
        # Create a container widget for the scroll area
        container_widget = QtWidgets.QWidget()
        scroll_area.setWidget(container_widget)

        # Create a layout for the container widget
        container_layout = QtWidgets.QGridLayout(container_widget)
        
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            row = 0
            for block in data.get("infoTab", []):
                group_box = QtWidgets.QGroupBox(block["group"])
                group_layout = QtWidgets.QVBoxLayout(group_box)
                
                # Add text
                text_label = QtWidgets.QLabel(block["text"])
                text_label.setWordWrap(True)
                group_layout.addWidget(text_label)
                
                # Add image if exists
                if 'image' in block and block["image"]:
                    image_path = os.path.join(pictures_folder, block["image"])
                    if os.path.exists(image_path):
                        pixmap = QPixmap(image_path)
                        image_label = QtWidgets.QLabel()
                        image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio))
                        group_layout.addWidget(image_label)
                    else:
                        print(f"Image not found: {image_path}")  # Debugging log

                    # Add the group box to the layout
                    container_layout.addWidget(group_box, row, 2)
                    row += 1  # Move to the next row

        except Exception as e:
            error_label = QtWidgets.QLabel(f"Failed to load content: {e}")
            container_layout.addWidget(error_label, 0, 0)

        # Add the scroll area to the main layout of the Information tab
        self.info_layout = QtWidgets.QVBoxLayout(self.Information)
        self.info_layout.addWidget(scroll_area)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
