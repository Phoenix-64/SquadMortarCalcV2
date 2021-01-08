from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from time import sleep
import calc
import corr
import fi_sys


class Worker(QtCore.QThread):
    output = QtCore.pyqtSignal(float, float, float, float, int)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.paused = True

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, cords, vertical, amount):

        self.cords = cords
        self.vertical = vertical
        self.amount = amount
        self.start()

    def update(self):

        self.paused = False

    def run(self):

        cords = self.cords

        vertical = self.vertical
        amount = self.amount
        while not self.exiting:
            for i in range(1, (len(cords))):

                while self.paused is True:
                    sleep(0)
                base_units = calc.get_cords_base_units(cords, i)
                angel_mils = [-1, 0]

                if 50 < base_units[0] < 1250:
                    angel_mils = calc.mils_calc(base_units[0], vertical)
                if amount == 2:
                    if (i % 2) == 0:
                        self.output.emit(angel_mils[0], calc.angle_deg_north(base_units[1]),
                                         base_units[0], angel_mils[1], int(i))
                    else:
                        self.output.emit(angel_mils[0], calc.angle_deg_north(base_units[1]),
                                         base_units[0], angel_mils[1], int(i))
                else:
                    self.output.emit(angel_mils[0], calc.angle_deg_north(base_units[1]),
                                     base_units[0], angel_mils[1], int(i))
                self.paused = True


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(796, 591)
        self.thread = Worker()

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.mortar_slider_horizontal = QtWidgets.QSlider(self.centralwidget)
        self.mortar_slider_horizontal.setGeometry(QtCore.QRect(27, 220, 110, 22))
        self.mortar_slider_horizontal.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mortar_slider_horizontal.setMaximum(33)
        self.mortar_slider_horizontal.setOrientation(QtCore.Qt.Horizontal)
        self.mortar_slider_horizontal.setObjectName("mortar_slider_horizontal")
        self.mortar_slider_vertical = QtWidgets.QSlider(self.centralwidget)
        self.mortar_slider_vertical.setGeometry(QtCore.QRect(150, 100, 22, 110))
        self.mortar_slider_vertical.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mortar_slider_vertical.setMaximum(33)
        self.mortar_slider_vertical.setOrientation(QtCore.Qt.Vertical)
        self.mortar_slider_vertical.setObjectName("mortar_slider_vertical")
        self.mortar_position_label = QtWidgets.QLabel(self.centralwidget)
        self.mortar_position_label.setGeometry(QtCore.QRect(20, 10, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.mortar_position_label.setFont(font)
        self.mortar_position_label.setAutoFillBackground(False)
        self.mortar_position_label.setObjectName("mortar_position_label")
        self.mortar_grid_label = QtWidgets.QLabel(self.centralwidget)
        self.mortar_grid_label.setGeometry(QtCore.QRect(20, 40, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mortar_grid_label.setFont(font)
        self.mortar_grid_label.setObjectName("mortar_grid_label")
        self.mortar_grid_input = QtWidgets.QLineEdit(self.centralwidget)
        self.mortar_grid_input.setGeometry(QtCore.QRect(20, 60, 113, 20))
        self.mortar_grid_input.setObjectName("mortar_grid_input")
        self.mortar_grid_img = QtWidgets.QLabel(self.centralwidget)
        self.mortar_grid_img.setGeometry(QtCore.QRect(21, 89, 121, 131))
        self.mortar_grid_img.setText("")
        self.mortar_grid_img.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\grid.png"))
        self.mortar_grid_img.setObjectName("mortar_grid_img")
        self.target_position_label = QtWidgets.QLabel(self.centralwidget)
        self.target_position_label.setGeometry(QtCore.QRect(200, 10, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.target_position_label.setFont(font)
        self.target_position_label.setAutoFillBackground(False)
        self.target_position_label.setObjectName("target_position_label")
        self.target_grid_input = QtWidgets.QLineEdit(self.centralwidget)
        self.target_grid_input.setGeometry(QtCore.QRect(200, 60, 113, 20))
        self.target_grid_input.setObjectName("target_grid_input")
        self.target_1_grid_img = QtWidgets.QLabel(self.centralwidget)
        self.target_1_grid_img.setGeometry(QtCore.QRect(201, 79, 161, 151))
        self.target_1_grid_img.setText("")
        self.target_1_grid_img.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\grid.png"))
        self.target_1_grid_img.setObjectName("target_1_grid_img")
        self.targed_grid_label = QtWidgets.QLabel(self.centralwidget)
        self.targed_grid_label.setGeometry(QtCore.QRect(200, 40, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.targed_grid_label.setFont(font)
        self.targed_grid_label.setObjectName("targed_grid_label")
        self.target_2_grid_img = QtWidgets.QLabel(self.centralwidget)
        self.target_2_grid_img.setGeometry(QtCore.QRect(381, 89, 121, 131))
        self.target_2_grid_img.setText("")
        self.target_2_grid_img.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\grid.png"))
        self.target_2_grid_img.setObjectName("target_2_grid_img")
        self.target_2_grid_label = QtWidgets.QLabel(self.centralwidget)
        self.target_2_grid_label.setGeometry(QtCore.QRect(380, 40, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.target_2_grid_label.setFont(font)
        self.target_2_grid_label.setObjectName("target_2_grid_label")
        self.target_position_2_label = QtWidgets.QLabel(self.centralwidget)
        self.target_position_2_label.setGeometry(QtCore.QRect(380, 10, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.target_position_2_label.setFont(font)
        self.target_position_2_label.setAutoFillBackground(False)
        self.target_position_2_label.setObjectName("target_position_2_label")
        self.target_2_grid_input = QtWidgets.QLineEdit(self.centralwidget)
        self.target_2_grid_input.setGeometry(QtCore.QRect(380, 60, 113, 20))
        self.target_2_grid_input.setObjectName("target_2_grid_input")
        self.target_1_line_horizontal = QtWidgets.QLabel(self.centralwidget)
        self.target_1_line_horizontal.setGeometry(QtCore.QRect(198, 195, 121, 16))
        self.target_1_line_horizontal.setText("")
        self.target_1_line_horizontal.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\line.png"))
        self.target_1_line_horizontal.setObjectName("target_1_line_horizontal")
        self.mortar_line_horizontal = QtWidgets.QLabel(self.centralwidget)
        self.mortar_line_horizontal.setGeometry(QtCore.QRect(20, 195, 121, 16))
        self.mortar_line_horizontal.setText("")
        self.mortar_line_horizontal.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\line.png"))
        self.mortar_line_horizontal.setObjectName("mortar_line_horizontal")
        self.target_2_line_horizontal = QtWidgets.QLabel(self.centralwidget)
        self.target_2_line_horizontal.setGeometry(QtCore.QRect(381, 195, 121, 16))
        self.target_2_line_horizontal.setText("")
        self.target_2_line_horizontal.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\line.png"))
        self.target_2_line_horizontal.setObjectName("target_2_line_horizontal")
        self.target_slider_vertical = QtWidgets.QSlider(self.centralwidget)
        self.target_slider_vertical.setGeometry(QtCore.QRect(330, 100, 22, 110))
        self.target_slider_vertical.setFocusPolicy(QtCore.Qt.NoFocus)
        self.target_slider_vertical.setMaximum(33)
        self.target_slider_vertical.setOrientation(QtCore.Qt.Vertical)
        self.target_slider_vertical.setObjectName("target_slider_vertical")
        self.target_2_slider_vertikal = QtWidgets.QSlider(self.centralwidget)
        self.target_2_slider_vertikal.setGeometry(QtCore.QRect(510, 100, 22, 110))
        self.target_2_slider_vertikal.setFocusPolicy(QtCore.Qt.NoFocus)
        self.target_2_slider_vertikal.setMaximum(33)
        self.target_2_slider_vertikal.setOrientation(QtCore.Qt.Vertical)
        self.target_2_slider_vertikal.setObjectName("target_2_slider_vertikal")
        self.target_slider_horizontal = QtWidgets.QSlider(self.centralwidget)
        self.target_slider_horizontal.setGeometry(QtCore.QRect(207, 220, 110, 22))
        self.target_slider_horizontal.setFocusPolicy(QtCore.Qt.NoFocus)
        self.target_slider_horizontal.setMaximum(33)
        self.target_slider_horizontal.setOrientation(QtCore.Qt.Horizontal)
        self.target_slider_horizontal.setObjectName("target_slider_horizontal")
        self.target_2_slider_horizontal = QtWidgets.QSlider(self.centralwidget)
        self.target_2_slider_horizontal.setGeometry(QtCore.QRect(387, 220, 110, 22))
        self.target_2_slider_horizontal.setFocusPolicy(QtCore.Qt.NoFocus)
        self.target_2_slider_horizontal.setMaximum(33)
        self.target_2_slider_horizontal.setOrientation(QtCore.Qt.Horizontal)
        self.target_2_slider_horizontal.setObjectName("target_2_slider_horizontal")
        self.mortar_line_vertikal = QtWidgets.QLabel(self.centralwidget)
        self.mortar_line_vertikal.setGeometry(QtCore.QRect(31, 96, 16, 117))
        self.mortar_line_vertikal.setText("")
        self.mortar_line_vertikal.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\line_vertikal.png"))
        self.mortar_line_vertikal.setObjectName("mortar_line_vertikal")
        self.target_1_line_vertikal = QtWidgets.QLabel(self.centralwidget)
        self.target_1_line_vertikal.setGeometry(QtCore.QRect(211, 96, 16, 117))
        self.target_1_line_vertikal.setText("")
        self.target_1_line_vertikal.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\line_vertikal.png"))
        self.target_1_line_vertikal.setObjectName("target_1_line_vertikal")
        self.target_2_line_vertikal = QtWidgets.QLabel(self.centralwidget)
        self.target_2_line_vertikal.setGeometry(QtCore.QRect(391, 95, 16, 117))
        self.target_2_line_vertikal.setText("")
        self.target_2_line_vertikal.setPixmap(QtGui.QPixmap("D:\\Programming\\SquadMortarCalcV2\\line_vertikal.png"))
        self.target_2_line_vertikal.setObjectName("target_2_line_vertikal")
        self.fire_order_label = QtWidgets.QLabel(self.centralwidget)
        self.fire_order_label.setGeometry(QtCore.QRect(340, 280, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.fire_order_label.setFont(font)
        self.fire_order_label.setAutoFillBackground(False)
        self.fire_order_label.setObjectName("fire_order_label")
        self.fire_order_1_label = QtWidgets.QLabel(self.centralwidget)
        self.fire_order_1_label.setGeometry(QtCore.QRect(340, 310, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fire_order_1_label.setFont(font)
        self.fire_order_1_label.setObjectName("fire_order_1_label")
        self.mils_label = QtWidgets.QLabel(self.centralwidget)
        self.mils_label.setGeometry(QtCore.QRect(340, 330, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mils_label.setFont(font)
        self.mils_label.setObjectName("mils_label")
        self.mils_output = QtWidgets.QLabel(self.centralwidget)
        self.mils_output.setGeometry(QtCore.QRect(340, 350, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.mils_output.setFont(font)
        self.mils_output.setObjectName("mils_output")
        self.heading_output = QtWidgets.QLabel(self.centralwidget)
        self.heading_output.setGeometry(QtCore.QRect(340, 390, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.heading_output.setFont(font)
        self.heading_output.setObjectName("heading_output")
        self.heading_label = QtWidgets.QLabel(self.centralwidget)
        self.heading_label.setGeometry(QtCore.QRect(340, 370, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.heading_label.setFont(font)
        self.heading_label.setObjectName("heading_label")
        self.distance_label = QtWidgets.QLabel(self.centralwidget)
        self.distance_label.setGeometry(QtCore.QRect(340, 410, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.distance_label.setFont(font)
        self.distance_label.setObjectName("distance_label")
        self.distance_output = QtWidgets.QLabel(self.centralwidget)
        self.distance_output.setGeometry(QtCore.QRect(340, 430, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.distance_output.setFont(font)
        self.distance_output.setObjectName("distance_output")
        self.fire_order_2_label = QtWidgets.QLabel(self.centralwidget)
        self.fire_order_2_label.setGeometry(QtCore.QRect(430, 310, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fire_order_2_label.setFont(font)
        self.fire_order_2_label.setObjectName("fire_order_2_label")
        self.heading_2_label = QtWidgets.QLabel(self.centralwidget)
        self.heading_2_label.setGeometry(QtCore.QRect(430, 370, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.heading_2_label.setFont(font)
        self.heading_2_label.setObjectName("heading_2_label")
        self.mils_2_output = QtWidgets.QLabel(self.centralwidget)
        self.mils_2_output.setGeometry(QtCore.QRect(430, 350, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.mils_2_output.setFont(font)
        self.mils_2_output.setObjectName("mils_2_output")
        self.distance_2_output = QtWidgets.QLabel(self.centralwidget)
        self.distance_2_output.setGeometry(QtCore.QRect(430, 430, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.distance_2_output.setFont(font)
        self.distance_2_output.setObjectName("distance_2_output")
        self.heading_2_output = QtWidgets.QLabel(self.centralwidget)
        self.heading_2_output.setGeometry(QtCore.QRect(430, 390, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.heading_2_output.setFont(font)
        self.heading_2_output.setObjectName("heading_2_output")
        self.mils_2_label = QtWidgets.QLabel(self.centralwidget)
        self.mils_2_label.setGeometry(QtCore.QRect(430, 330, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.mils_2_label.setFont(font)
        self.mils_2_label.setObjectName("mils_2_label")
        self.distance_2_label = QtWidgets.QLabel(self.centralwidget)
        self.distance_2_label.setGeometry(QtCore.QRect(430, 410, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.distance_2_label.setFont(font)
        self.distance_2_label.setObjectName("distance_2_label")
        self.correction_label = QtWidgets.QLabel(self.centralwidget)
        self.correction_label.setGeometry(QtCore.QRect(580, 280, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.correction_label.setFont(font)
        self.correction_label.setAutoFillBackground(False)
        self.correction_label.setObjectName("correction_label")
        self.farther_label = QtWidgets.QLabel(self.centralwidget)
        self.farther_label.setGeometry(QtCore.QRect(580, 310, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.farther_label.setFont(font)
        self.farther_label.setObjectName("farther_label")
        self.farther_input = QtWidgets.QSpinBox(self.centralwidget)
        self.farther_input.setGeometry(QtCore.QRect(580, 330, 42, 22))
        self.farther_input.setFocusPolicy(QtCore.Qt.NoFocus)
        self.farther_input.setMinimum(-99)
        self.farther_input.setObjectName("farther_input")
        self.left_input = QtWidgets.QSpinBox(self.centralwidget)
        self.left_input.setGeometry(QtCore.QRect(660, 330, 42, 22))
        self.left_input.setFocusPolicy(QtCore.Qt.NoFocus)
        self.left_input.setMinimum(-99)
        self.left_input.setObjectName("left_input")
        self.left_label = QtWidgets.QLabel(self.centralwidget)
        self.left_label.setGeometry(QtCore.QRect(660, 310, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.left_label.setFont(font)
        self.left_label.setObjectName("left_label")
        self.mode_settings_label = QtWidgets.QLabel(self.centralwidget)
        self.mode_settings_label.setGeometry(QtCore.QRect(570, 10, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.mode_settings_label.setFont(font)
        self.mode_settings_label.setAutoFillBackground(False)
        self.mode_settings_label.setObjectName("mode_settings_label")
        self.amount_label = QtWidgets.QLabel(self.centralwidget)
        self.amount_label.setGeometry(QtCore.QRect(570, 40, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.amount_label.setFont(font)
        self.amount_label.setObjectName("amount_label")
        self.amount_input = QtWidgets.QSpinBox(self.centralwidget)
        self.amount_input.setGeometry(QtCore.QRect(570, 60, 42, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.amount_input.setFont(font)
        self.amount_input.setFocusPolicy(QtCore.Qt.NoFocus)
        self.amount_input.setMinimum(1)
        self.amount_input.setMaximum(2)
        self.amount_input.setObjectName("amount_input")
        self.fire_mode_input = QtWidgets.QComboBox(self.centralwidget)
        self.fire_mode_input.setGeometry(QtCore.QRect(570, 110, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.fire_mode_input.setFont(font)
        self.fire_mode_input.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.fire_mode_input.setObjectName("fire_mode_input")
        self.fire_mode_input.addItem("")
        self.fire_mode_input.addItem("")
        self.fire_mode_input.addItem("")
        self.fire_mode_label = QtWidgets.QLabel(self.centralwidget)
        self.fire_mode_label.setGeometry(QtCore.QRect(570, 90, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fire_mode_label.setFont(font)
        self.fire_mode_label.setObjectName("fire_mode_label")
        self.fire_data_label = QtWidgets.QLabel(self.centralwidget)
        self.fire_data_label.setGeometry(QtCore.QRect(140, 280, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.fire_data_label.setFont(font)
        self.fire_data_label.setAutoFillBackground(False)
        self.fire_data_label.setObjectName("fire_data_label")
        self.rounds_label = QtWidgets.QLabel(self.centralwidget)
        self.rounds_label.setGeometry(QtCore.QRect(140, 310, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rounds_label.setFont(font)
        self.rounds_label.setObjectName("rounds_label")
        self.rounds_output = QtWidgets.QLabel(self.centralwidget)
        self.rounds_output.setGeometry(QtCore.QRect(140, 330, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.rounds_output.setFont(font)
        self.rounds_output.setObjectName("rounds_output")
        self.fligth_label = QtWidgets.QLabel(self.centralwidget)
        self.fligth_label.setGeometry(QtCore.QRect(140, 350, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fligth_label.setFont(font)
        self.fligth_label.setObjectName("fligth_label")
        self.fligth_output = QtWidgets.QLabel(self.centralwidget)
        self.fligth_output.setGeometry(QtCore.QRect(140, 370, 200, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.fligth_output.setFont(font)
        self.fligth_output.setObjectName("fligth_output")
        self.vertical_seperation_label = QtWidgets.QLabel(self.centralwidget)
        self.vertical_seperation_label.setGeometry(QtCore.QRect(570, 190, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.vertical_seperation_label.setFont(font)
        self.vertical_seperation_label.setObjectName("vertical_seperation_label")
        self.roun_output = QtWidgets.QLabel(self.centralwidget)
        self.roun_output.setGeometry(QtCore.QRect(340, 470, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.roun_output.setFont(font)
        self.roun_output.setObjectName("roun_output")
        self.round_label = QtWidgets.QLabel(self.centralwidget)
        self.round_label.setGeometry(QtCore.QRect(340, 450, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.round_label.setFont(font)
        self.round_label.setObjectName("round_label")
        self.round_2_output = QtWidgets.QLabel(self.centralwidget)
        self.round_2_output.setGeometry(QtCore.QRect(430, 470, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.round_2_output.setFont(font)
        self.round_2_output.setObjectName("round_2_output")
        self.round_2_label = QtWidgets.QLabel(self.centralwidget)
        self.round_2_label.setGeometry(QtCore.QRect(430, 450, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.round_2_label.setFont(font)
        self.round_2_label.setObjectName("round_2_label")
        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(350, 500, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.time_label.setFont(font)
        self.time_label.setObjectName("time_label")
        self.time_output = QtWidgets.QLabel(self.centralwidget)
        self.time_output.setGeometry(QtCore.QRect(354, 520, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.time_output.setFont(font)
        self.time_output.setObjectName("time_output")
        self.vertical_seperation_input = QtWidgets.QSpinBox(self.centralwidget)
        self.vertical_seperation_input.setGeometry(QtCore.QRect(570, 210, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.vertical_seperation_input.setFont(font)
        self.vertical_seperation_input.setFocusPolicy(QtCore.Qt.NoFocus)
        self.vertical_seperation_input.setMinimum(-200)
        self.vertical_seperation_input.setMaximum(200)
        self.vertical_seperation_input.setObjectName("vertical_seperation_input")
        self.auto_label = QtWidgets.QLabel(self.centralwidget)
        self.auto_label.setGeometry(QtCore.QRect(570, 140, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auto_label.setFont(font)
        self.auto_label.setObjectName("auto_label")
        self.auto_input = QtWidgets.QComboBox(self.centralwidget)
        self.auto_input.setGeometry(QtCore.QRect(570, 160, 71, 22))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.auto_input.setFont(font)
        self.auto_input.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.auto_input.setObjectName("auto_input")
        self.auto_input.addItem("")
        self.auto_input.addItem("")
        self.fire = QtWidgets.QPushButton(self.centralwidget)
        self.fire.setGeometry(QtCore.QRect(140, 410, 111, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.fire.setFont(font)
        self.fire.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.fire.setObjectName("fire")
        self.status_output = QtWidgets.QLabel(self.centralwidget)
        self.status_output.setGeometry(QtCore.QRect(140, 510, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.status_output.setFont(font)
        self.status_output.setObjectName("status_output")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(140, 490, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.shot_time_label = QtWidgets.QLabel(self.centralwidget)
        self.shot_time_label.setGeometry(QtCore.QRect(570, 240, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_time_label.setFont(font)
        self.shot_time_label.setObjectName("shot_time_label")
        self.shot_time_input = QtWidgets.QSpinBox(self.centralwidget)
        self.shot_time_input.setGeometry(QtCore.QRect(570, 260, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shot_time_input.setFont(font)
        self.shot_time_input.setFocusPolicy(QtCore.Qt.NoFocus)
        self.shot_time_input.setMinimum(1)
        self.shot_time_input.setMaximum(40)
        self.shot_time_input.setObjectName("shot_time_input")

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        # self.thread.output['int', "int", "int", "int", "float"].connect(self.fire_manual)
        self.thread.output.connect(self.fire_manual)

        self.fire.clicked.connect(self.thread.update)
        self.fire.clicked.connect(lambda: self.fire_calculation(True))

        self.mortar_grid_input.textChanged.connect(lambda: self.fire_calculation())
        self.target_grid_input.textChanged.connect(lambda: self.fire_calculation())
        self.target_2_grid_input.textChanged.connect(lambda: self.fire_calculation())

        self.fire_mode_input.currentIndexChanged.connect(lambda: self.fire_calculation())
        self.auto_input.currentIndexChanged.connect(lambda: self.fire_calculation())
        self.amount_input.valueChanged.connect(lambda: self.fire_calculation())
        self.vertical_seperation_input.valueChanged.connect(lambda: self.fire_calculation())
        self.shot_time_input.valueChanged.connect(lambda: self.fire_calculation())

        self.mortar_slider_horizontal.valueChanged.connect(lambda: self.slider_update(10))
        self.mortar_slider_vertical.valueChanged.connect(lambda: self.slider_update(11))
        self.target_slider_vertical.valueChanged.connect(lambda: self.slider_update(21))
        self.target_slider_horizontal.valueChanged.connect(lambda: self.slider_update(20))
        self.target_2_slider_vertikal.valueChanged.connect(lambda: self.slider_update(31))
        self.target_2_slider_horizontal.valueChanged.connect(lambda: self.slider_update(30))
        # todo: implement slider readonly (https://stackoverflow.com/questions/22844649/pyqt-how-to-set-combobox-read-only)
        self.readonly = False

    def retranslateUi(self, MainWindow):
        global firePaused
        firePaused = False
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("main_window", "Squad Mortar Calculator"))
        self.mortar_position_label.setText(_translate("main_window", "Mortar Position:"))
        self.mortar_grid_label.setText(_translate("main_window", "Grid:"))
        self.target_position_label.setText(_translate("main_window", "Target Position 1:"))
        self.targed_grid_label.setText(_translate("main_window", "Grid:"))
        self.target_2_grid_label.setText(_translate("main_window", "Grid:"))
        self.target_position_2_label.setText(_translate("main_window", "Target Position 2:"))
        self.fire_order_label.setText(_translate("main_window", "Fire Order:"))
        self.fire_order_1_label.setText(_translate("main_window", "Mortar 1:"))
        self.mils_label.setText(_translate("main_window", "Mils:"))
        self.mils_output.setText(_translate("main_window", "0"))
        self.heading_output.setText(_translate("main_window", "0"))
        self.heading_label.setText(_translate("main_window", "Heading:"))
        self.distance_label.setText(_translate("main_window", "Distance:"))
        self.distance_output.setText(_translate("main_window", "0"))
        self.fire_order_2_label.setText(_translate("main_window", "Mortar 2:"))
        self.heading_2_label.setText(_translate("main_window", "Heading:"))
        self.mils_2_output.setText(_translate("main_window", "0"))
        self.distance_2_output.setText(_translate("main_window", "0"))
        self.heading_2_output.setText(_translate("main_window", "0"))
        self.mils_2_label.setText(_translate("main_window", "Mils:"))
        self.distance_2_label.setText(_translate("main_window", "Distance:"))
        self.correction_label.setText(_translate("main_window", "Correction:"))
        self.farther_label.setText(_translate("main_window", "Distance:"))
        self.left_label.setText(_translate("main_window", "Angle:"))
        self.mode_settings_label.setText(_translate("main_window", "Mode Settings:"))
        self.amount_label.setText(_translate("main_window", "Mortar amount:"))
        self.fire_mode_input.setItemText(0, _translate("main_window", "Normal"))
        self.fire_mode_input.setItemText(1, _translate("main_window", "Line"))
        self.fire_mode_input.setItemText(2, _translate("main_window", "Area"))
        self.fire_mode_label.setText(_translate("main_window", "Fire mode:"))
        self.fire_data_label.setText(_translate("main_window", "Fire Data:"))
        self.rounds_label.setText(_translate("main_window", "Rounds:"))
        self.rounds_output.setText(_translate("main_window", "0"))
        self.fligth_label.setText(_translate("main_window", "Time to Impact:"))
        self.fligth_output.setText(_translate("main_window", "0"))
        self.vertical_seperation_label.setText(_translate("main_window", "Vertical Seperation:"))
        self.roun_output.setText(_translate("main_window", "1"))
        self.round_label.setText(_translate("main_window", "Round:"))
        self.round_2_output.setText(_translate("main_window", "1"))
        self.round_2_label.setText(_translate("main_window", "Round:"))
        self.time_label.setText(_translate("main_window", "Time to last impact:"))
        self.time_output.setText(_translate("main_window", "0"))
        self.auto_label.setText(_translate("main_window", "Auto fire:"))
        self.auto_input.setItemText(0, _translate("main_window", "Off"))
        self.auto_input.setItemText(1, _translate("main_window", "On"))
        self.fire.setText(_translate("main_window", "FIRE!"))
        self.status_output.setText(_translate("main_window", "Calculating"))
        self.status_label.setText(_translate("main_window", "Status:"))
        self.shot_time_label.setText(_translate("main_window", "Time per Shot:"))
        self.shot_time_input.setValue(4)

    def block_inputs(self):
        self.vertical_seperation_input.setReadOnly(True)
        self.shot_time_input.setReadOnly(True)
        self.farther_input.setReadOnly(True)
        self.left_input.setReadOnly(True)
        self.mortar_grid_input.setReadOnly(True)
        self.target_grid_input.setReadOnly(True)
        self.target_2_grid_input.setReadOnly(True)
        self.fire.setEnabled(False)
        self.auto_input.setEnabled(False)
        self.fire_mode_input.setEnabled(False)
        self.auto_input.setEnabled(False)

    def allow_inputs(self):
        self.vertical_seperation_input.setReadOnly(False)
        self.shot_time_input.setReadOnly(False)
        self.farther_input.setReadOnly(False)
        self.left_input.setReadOnly(False)
        self.mortar_grid_input.setReadOnly(False)
        self.target_grid_input.setReadOnly(False)
        self.target_2_grid_input.setReadOnly(False)
        self.fire.setEnabled(True)
        self.auto_input.setEnabled(True)
        self.fire_mode_input.setEnabled(True)
        self.auto_input.setEnabled(True)

    def update_main(self, mils, heading, distance, time, shot=1):
        self.mils_output.setText(str(mils))
        self.heading_output.setText(str(round(heading)))
        self.distance_output.setText(str(round(distance)))
        self.fligth_output.setText(str(round(time, 1)))
        self.roun_output.setText(str(shot))

    def update_second(self, mils, heading, distance, shot=1):
        self.mils_2_output.setText(str(mils))
        self.heading_2_output.setText(str(round(heading)))
        self.distance_2_output.setText(str(round(distance)))
        self.roun_output.setText(str(shot))

    def fire_manual(self, mils, heading, distance, time, i):
        if mils == -1:
            mils = "Out of Range"
        if self.amount_input.value() == 1:
            self.update_main(mils, calc.angle_deg_north(heading), distance, time, i)
            self.update_second(mils, calc.angle_deg_north(heading), distance, i)
        else:
            if i % 2 == 0:
                self.update_main(mils, calc.angle_deg_north(heading), distance, time, i)
            else:
                self.update_second(mils, calc.angle_deg_north(heading), distance, i)
        return

    def auto_fire(self, cords, i):
        if self.auto_input.currentText() == "Off":
            return
        base_units = calc.get_cords_base_units(cords, i)
        angel_mils = ["Out of range", 0]
        # time = 0

        if 50 < base_units[0] < 1250:
            angel_mils = calc.mils_calc(base_units[0], self.vertical_seperation_input.value())
        if self.amount_input.value() == 2:
            if (i % 2) == 0:
                self.update_main(angel_mils[0], calc.angle_deg_north(base_units[1]), base_units[0], angel_mils[1], i)
                return
            else:
                self.update_second(angel_mils[0], calc.angle_deg_north(base_units[1]), base_units[0], i)
                return
        else:
            self.update_main(angel_mils[0], calc.angle_deg_north(base_units[0]), base_units[0], angel_mils[1], i)
            self.update_second(angel_mils[0], calc.angle_deg_north(base_units[0]), base_units[0], i)
        return

    def fire_order(self, cords, cords3=None, fire_mode="Normal", button=False):

        angel_mi = "Out of range"
        time = 0
        shot_time = self.shot_time_input.value() * 1000
        if fire_mode == "Normal":

            base_units = calc.get_cords_base_units(cords)
            base_units[0] = corr.distance_cor(base_units[0], self.farther_input.text())
            base_units[1] = corr.angle_cor(base_units[1], base_units[0], self.left_input.text())

            if 50 < base_units[0] < 1250:
                angel_mils, time = calc.mils_calc(base_units[0], self.vertical_seperation_input.value())
            self.update_main(angel_mils, calc.angle_deg_north(base_units[1]), base_units[0], time)

        elif fire_mode == "Line":
            cords.extend(fi_sys.lineFire(cords[1], cords3))
            self.rounds_output.setText(str(len(cords) - 1))

            if self.auto_input.currentText() == "On" and button is True:
                self.status_output.setText("Firing!")
                self.block_inputs()
                for i in range(1, (len(cords))):
                    QtCore.QTimer.singleShot(shot_time * i, partial(self.auto_fire, cords, i))
                self.status_output.setText("Calculating")
                self.allow_inputs()
            else:
                self.status_output.setText("Firing!")

                self.thread.render(cords, self.vertical_seperation_input.value(), self.amount_input.value())
        elif fire_mode == "Area":
            cords.extend(fi_sys.areaFire(cords[1], cords3))
            self.rounds_output.setText((str(len(cords) - 1)))

            if self.auto_input.currentText() == "On" and button is True:
                self.status_output.setText("Firing!")
                self.block_inputs()
                for i in range(1, (len(cords))):
                    QtCore.QTimer.singleShot(shot_time * i, partial(self.auto_fire, cords, i))
                self.status_output.setText("Calculating")
                self.allow_inputs()
            else:
                self.status_output.setText("Firing!")

                self.thread.render(cords, self.vertical_seperation_input.value(), self.amount_input.value())

    def fire_calculation(self, button=False):

        if self.mortar_grid_input.text() != "" and self.target_grid_input.text() != "":
            cords = [self.mortar_grid_input.text(), self.target_grid_input.text()]

            try:
                cords = [calc.look_up(calc.split_cord(str)) for str in cords]
            except ValueError:
                return
            cords[0] = corr.add_slider(cords[0], self.mortar_slider_horizontal.value(),
                                       self.mortar_slider_vertical.value())
            cords[1] = corr.add_slider(cords[1], self.target_slider_horizontal.value(),
                                       self.target_slider_vertical.value())

            fire_mode = str(self.fire_mode_input.currentText())
            if self.target_2_grid_input.text() != "" and fire_mode != "Normal":
                cord3 = self.target_2_grid_input.text()
                try:
                    cord3 = calc.look_up(calc.split_cord(cord3))
                except ValueError:
                    return
                cord3 = corr.add_slider(cord3, self.mortar_slider_horizontal.value(),
                                        self.mortar_slider_vertical.value())

                if fire_mode == "Line":

                    self.fire_order(cords, cord3, fire_mode, button)
                elif fire_mode == "Area":
                    self.fire_order(cords, cord3, fire_mode, button)
            else:
                self.fire_order(cords, button=button)

        else:
            return

    def slider_update(self, img):
        if img == 10:
            self.mortar_line_vertikal.setGeometry(
                QtCore.QRect(31 + int(self.mortar_slider_horizontal.value() * 2.9696), 96, 16, 117))
        elif img == 11:
            self.mortar_line_horizontal.setGeometry(
                QtCore.QRect(20, 195 - int(self.mortar_slider_vertical.value() * 2.9696), 121, 16))
        elif img == 20:
            self.target_1_line_vertikal.setGeometry(
                QtCore.QRect(211 + int(self.target_slider_horizontal.value() * 2.9696), 96, 16, 117))
        elif img == 21:
            self.target_1_line_horizontal.setGeometry(
                QtCore.QRect(198, 195 - int(self.target_slider_vertical.value() * 2.9696), 121, 16))
        elif img == 30:
            self.target_2_line_vertikal.setGeometry(
                QtCore.QRect(391 + int(self.target_2_slider_horizontal.value() * 2.9696), 95, 16, 117))
        elif img == 31:
            self.target_2_line_horizontal.setGeometry(
                QtCore.QRect(381, 195 - int(self.target_2_slider_vertikal.value() * 2.9696), 121, 16))
        self.fire_calculation()
        return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
