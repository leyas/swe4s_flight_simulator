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

from src.drivers.rocketDrawing import RocketDrawing  # Custom drawing class
from src.drivers.aeroCalcs import AeroCalcs  # Aero calculations
from src.drivers.physCalcs import PhysCalcs

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.json_path = os.path.join(os.path.dirname(__file__), "src\\config\\rocket_specs.json")
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

        self.material_label = QtWidgets.QLabel("Material:")
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

        self.parachute_label = QtWidgets.QLabel("Sizes:")
        self.parachute_label.setFont(label_font)
        self.parachute_list = QtWidgets.QListWidget()
        for item in ["Small", "Medium", "Larger"]:
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

        # Add information Tab to Tab Widget
        self.tabWidget.addTab(self.Information, "Information Tab")

        self.setup_info_tab(screen_height)

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
        # Air frame connections
        self.af_d_input.valueChanged.connect(self.update_af_diameter)
        self.af_l_input.valueChanged.connect(self.update_af_length)

        # Nose Cone connections
        self.nc_l_input.valueChanged.connect(self.update_nc_length)
        self.nc_list.itemClicked.connect(self.update_nc_shape)

        # Fins connections
        self.sweep_angle_input.valueChanged.connect(self.update_sweep_angle)
        self.tip_chord_input.valueChanged.connect(self.update_tip_chord)
        self.semi_span_input.valueChanged.connect(self.update_semi_span)
        self.root_chord_input.valueChanged.connect(self.update_root_chord)

        # Materials connections
        self.material_list.itemClicked.connect(self.update_material)

        # Motors connections
        self.motor_list.itemClicked.connect(self.update_motor)

        # Parachute connections
        self.parachute_list.itemClicked.connect(self.update_parachute)

    def update_json(self, section, key, value):
        """Update the JSON file with the specified key-value pair."""
        
        try:
            with open(self.json_path, "r") as file:
                data = json.load(file)

            if section in data and key in data[section]:
                data[section][key] = value

            with open(self.json_path, "w") as file:
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

    def update_parachute(self, parachute_size):
        size = parachute_size.text().lower()
        if size == "small":
            self.update_json("parachute", "cd", 1.25)
            self.update_json("parachute", "mass", 60)
        elif size == "medium":
            self.update_json("parachute", "cd", 1.5)
            self.update_json("parachute", "mass", 70)
        else: 
            self.update_json("parachute", "cd", 1.8)
            self.update_json("parachute", "mass", 127.6)

    def update_material(self, material):
        mat = material.text().lower()
        if mat == "fiberglass":
            self.update_json("material", "density", 1.8)
            self.update_json("material", "thickness", 3)
        else: 
            self.update_json("material", "density", 1.15)
            self.update_json("material", "thickness", 3)

    def update_motor(self, motor):
        mot = motor.text().lower()
        if mot == "g":
            self.update_json("motor", "thrust", 10)
            self.update_json("motor", "burn_time", 2.5)
            self.update_json("motor", "mass", 100)
            self.update_json("motor", "length", 4)
            self.update_json("motor", "diameter", 1)

        elif mot == "h":
            self.update_json("motor", "thrust", 100)
            self.update_json("motor", "burn_time", 2.75)
            self.update_json("motor", "mass", 200)
            self.update_json("motor", "length", 6)
            self.update_json("motor", "diameter", 1.5)
        
        elif mot == "i":
            self.update_json("motor", "thrust", 200)
            self.update_json("motor", "burn_time", 3)
            self.update_json("motor", "mass", 300)
            self.update_json("motor", "length", 8)
            self.update_json("motor", "diameter", 2)
        
        elif mot == "j":
            self.update_json("motor", "thrust", 400)
            self.update_json("motor", "burn_time", 3.25)
            self.update_json("motor", "mass", 400)
            self.update_json("motor", "length", 9)
            self.update_json("motor", "diameter", 2.5)
        
        elif mot == "k":
            self.update_json("motor", "thrust", 800)
            self.update_json("motor", "burn_time", 3.5)
            self.update_json("motor", "mass", 500)
            self.update_json("motor", "length", 10)
            self.update_json("motor", "diameter", 3)

        else: # L
            self.update_json("motor", "thrust", 1600)
            self.update_json("motor", "burn_time", 3.75)
            self.update_json("motor", "mass", 600)
            self.update_json("motor", "length", 11)
            self.update_json("motor", "diameter", 3.5)


    def display_rocket_design(self):
        """
        Display the rocket design in the embedded Matplotlib graph.
        """
        self.design_figure.clear()
        ax = self.design_figure.add_subplot(111)

        # Load the rocket specs JSON
        with open(self.json_path, "r") as file:
            rocket_specs = json.load(file)

        # Create an instance of AeroCalcs to calculate CG and CP
        aero_calcs = AeroCalcs(rocket_specs)
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

        phys_calcs = PhysCalcs(self.json_path)
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

    def setup_info_tab(self, screen_height, ):
        """ Sets up info tab based on json file"""
        info_path = os.path.join(os.path.dirname(__file__), "src\\config\\info_content.json")
        pictures_folder = os.path.join(os.path.dirname(__file__), "src\\pictures")
        
        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea(self.Information)
        scroll_area.setWidgetResizable(True)
        
        # Create a container widget for the scroll area
        container_widget = QtWidgets.QWidget()
        scroll_area.setWidget(container_widget)
        scroll_area.setStyleSheet("background-color: white;")

        # Create a layout for the container widget
        container_layout = QtWidgets.QGridLayout(container_widget)
        
        try:
            with open(info_path, 'r') as file:
                data = json.load(file)

            row = 0
            for block in data.get("infoTab", []):
                text_group_box = QtWidgets.QGroupBox(block["group"])
                text_group_box.setStyleSheet("QGroupBox { font-weight: bold; border: none; padding-top: 40px; }")
                group_font = text_group_box.font()
                group_font.setPointSize(int(screen_height * 0.006))
                text_group_box.setFont(group_font)
                text_group_layout = QtWidgets.QVBoxLayout(text_group_box)
                text_label = QtWidgets.QLabel(block["text"])
                text_label.setWordWrap(True)
                text_group_layout.addWidget(text_label)
                container_layout.addWidget(text_group_box, row, 0) 

                # Add image group box if an image exists
                if 'image' in block and block["image"]:
                    image_group_box = QtWidgets.QGroupBox()
                    image_group_box.setStyleSheet("QGroupBox { background-color: white; border: none;}")
                    image_group_layout = QtWidgets.QVBoxLayout(image_group_box)
                    image_path = os.path.join(pictures_folder, block["image"])
                    if os.path.exists(image_path):
                        pixmap = QPixmap(image_path)
                        image_label = QtWidgets.QLabel()
                        image_label.setPixmap(pixmap.scaled(int(3*screen_height/5), int(2*screen_height/5), QtCore.Qt.KeepAspectRatio))
                        image_group_layout.addWidget(image_label)
                    else:
                        print(f"Image not found: {image_path}")  # Debugging log

                    container_layout.addWidget(image_group_box, row, 1)
                row += 1
                


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
