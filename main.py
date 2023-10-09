import time
import cv2
import numpy as np
from PyQt5.QtCore import Qt,pyqtSignal,QThread
from PyQt5.QtWidgets import  QDialog, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import main_image as main_image
import sys
import formlist as formlist
import report as report_window
import ADD as ADD
import form_reco as form_reco
# import mysql.connector
import datetime
import pytz
import os
import uuid
from datetime import datetime, timedelta
from config import weights_detect,weights_reco
from sql import dbsql,cursor
# db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
#                              host='192.168.1.89', database='vehicle-identification')
# db= dbsql
cursor = cursor
groupID = 1
vehicle_company_id = 1
current_directory = os.getcwd()

# weights_detect=current_directory + r'\model\LP_detector_nano_61.pt'
# weights_reco = current_directory + r'\model\best_188.pt'
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = ''
detect= False

class Ui_MainWindow(object):
    global cursor
    def setupUi(self, MainWindow):
        global ui,cursor
        # self.db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
        #                      host='192.168.1.89', database='vehicle-identification')
        
        self.thread = {}
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(968, 657)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(2, 2, 2, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/newPrefix/image/2.png);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)


        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Buttonfile = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Buttonfile.sizePolicy().hasHeightForWidth())
        self.Buttonfile.setSizePolicy(sizePolicy)
        self.Buttonfile.setMaximumSize(QtCore.QSize(60, 50))
        self.Buttonfile.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/newPrefix/image/folder.png);")
        self.Buttonfile.setText("")
        self.Buttonfile.setObjectName("Buttonfile")
        self.horizontalLayout.addWidget(self.Buttonfile)
        self.Buttonfile.clicked.connect(self.button_f)

        self.Buttoncam = QtWidgets.QPushButton(self.centralwidget)
        self.Buttoncam.setMaximumSize(QtCore.QSize(60, 50))
        self.Buttoncam.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"image: url(:/newPrefix/image/camera.png);")
        self.Buttoncam.setText("")
        self.Buttoncam.setObjectName("Buttoncam")
        self.horizontalLayout.addWidget(self.Buttoncam)
        self.Buttoncam.clicked.connect(self.button_camera)

        self.combobox_list = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_list.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.combobox_list.setFont(font)
        self.combobox_list.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.combobox_list.setObjectName("combobox_list")
        self.horizontalLayout.addWidget(self.combobox_list)
        self.combobox_list.currentIndexChanged.connect(self.select_combobox)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.comboBox.currentIndexChanged.connect(self.select_combobox_RTSP)

        self.Button_baocao = QtWidgets.QPushButton(self.centralwidget)
        self.Button_baocao.setMaximumSize(QtCore.QSize(60, 50))
        self.Button_baocao.setStyleSheet("background-color: rgb(85, 255, 255);\n"
"image: url(:/newPrefix/image/menu.png);")
        self.Button_baocao.setText("")
        self.Button_baocao.setObjectName("Button_baocao")
        self.horizontalLayout.addWidget(self.Button_baocao)
        self.Button_baocao.clicked.connect(self.button_bc)

        self.Button_Reco = QtWidgets.QPushButton(self.centralwidget)
        self.Button_Reco.setMaximumSize(QtCore.QSize(60, 50))
        self.Button_Reco.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"image: url(:/newPrefix/image/car.png);")
        self.Button_Reco.setText("")
        self.Button_Reco.setObjectName("Button_Reco")
        self.horizontalLayout.addWidget(self.Button_Reco)
        self.Button_Reco.clicked.connect(self.button_LPR)

        self.Button_setting = QtWidgets.QPushButton(self.centralwidget)
        self.Button_setting.setMaximumSize(QtCore.QSize(60, 50))
        self.Button_setting.setStyleSheet("background-color: rgb(170, 255, 255);\n"
"image: url(:/newPrefix/image/settings.png);")
        self.Button_setting.setText("")
        self.Button_setting.setObjectName("Button_setting")
        self.horizontalLayout.addWidget(self.Button_setting)
        self.Button_setting.clicked.connect(self.button_setting)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(7)
        self.gridLayout.setObjectName("gridLayout")
        self.viewcam3 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam3.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.viewcam3.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam3.setScaledContents(True)
        self.viewcam3.setObjectName("viewcam3")
        self.gridLayout.addWidget(self.viewcam3, 4, 2, 1, 1)


        self.viewcam1 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam1.setStyleSheet("background-color: rgb(255, 255, 0);\n"
# "")
        self.viewcam1.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam1.setScaledContents(True)
        self.viewcam1.setObjectName("viewcam1")
        self.gridLayout.addWidget(self.viewcam1, 4, 0, 1, 1)


        self.viewcam5 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam5.setStyleSheet("background-color: rgb(255, 85, 127);")
        self.viewcam5.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam5.setScaledContents(True)
        self.viewcam5.setObjectName("viewcam5")
        self.gridLayout.addWidget(self.viewcam5, 5, 1, 1, 1)


        self.viewcam4 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam4.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.viewcam4.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam4.setScaledContents(True)
        self.viewcam4.setObjectName("viewcam4")
        self.gridLayout.addWidget(self.viewcam4, 5, 0, 1, 1)


        self.viewcam6 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam6.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.viewcam6.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam6.setScaledContents(True)
        self.viewcam6.setObjectName("viewcam6")
        self.gridLayout.addWidget(self.viewcam6, 5, 2, 1, 1)


        self.viewcam2 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam2.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.viewcam2.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam2.setScaledContents(True)
        self.viewcam2.setObjectName("viewcam2")
        self.gridLayout.addWidget(self.viewcam2, 4, 1, 1, 1)


        self.viewcam7 = QtWidgets.QLabel(self.centralwidget)
        self.viewcam7.setMouseTracking(False)
        # self.viewcam7.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.viewcam7.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam7.setScaledContents(True)
        self.viewcam7.setObjectName("viewcam7")
        self.gridLayout.addWidget(self.viewcam7, 6, 0, 1, 1)


        self.viewcam8 = QtWidgets.QLabel(self.centralwidget)
#         self.viewcam8.setStyleSheet("\n"
# "background-color: rgb(170, 170, 0);")
        self.viewcam8.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam8.setScaledContents(True)
        self.viewcam8.setObjectName("viewcam8")
        self.gridLayout.addWidget(self.viewcam8, 6, 1, 1, 1)


        self.viewcam9 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam9.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.viewcam9.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam9.setFrameShadow(QtWidgets.QFrame.Plain)
        self.viewcam9.setLineWidth(1)
        self.viewcam9.setScaledContents(True)
        self.viewcam9.setObjectName("viewcam9")
        self.gridLayout.addWidget(self.viewcam9, 6, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.verticalLayout.addLayout(self.gridLayout)
        self.viewcam1.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam4.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam5.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam6.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam7.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam8.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.viewcam9.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.current_fullscreen_index = None

        self.Dialog = MainWindow
        self.viewcam1.mousePressEvent = self.fullscreen_viewcam1
        self.viewcam2.mousePressEvent = self.fullscreen_viewcam2
        self.viewcam3.mousePressEvent = self.fullscreen_viewcam3
        self.viewcam4.mousePressEvent = self.fullscreen_viewcam4
        self.viewcam5.mousePressEvent = self.fullscreen_viewcam5
        self.viewcam6.mousePressEvent = self.fullscreen_viewcam6
        self.viewcam7.mousePressEvent = self.fullscreen_viewcam7
        self.viewcam8.mousePressEvent = self.fullscreen_viewcam8
        self.viewcam9.mousePressEvent = self.fullscreen_viewcam9
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.is_fullscreen = False  # Add this attribute to track fullscreen state
        self.fullscreen_dialog = None 
        self.start_capture_video()
        self.load_data_to_combobox_list_and_rtsp()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    def load_data_to_combobox_list_and_rtsp(self):
        # self.db = mysql.connector.connect(user='root', password='12345678',
        #                      host='127.0.0.1', database='aipt')
        # self.db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
        #                      host='192.168.1.89', database='vehicle-identification')
        
        # cursor = db.cursor()
        cursor.execute("SELECT name FROM listsvehicle WHERE status = 1")
        results = cursor.fetchall()
        
        # Xóa dữ liệu cũ từ QComboBox
        # self.comboBox_listxe.clear()

        # Thêm dữ liệu từ cơ sở dữ liệu vào QComboBox
        for result in results:
            self.combobox_list.addItem(result[0])

        cursor.close()
    
    def fullscreen_viewcam1(self, event):
        if not self.is_fullscreen:
            # Store the current row and column positions
            # self.saved_row, self.saved_col = self.gridLayout.getposition(self.viewcam1)

            # Remove the widget from the layout
            self.gridLayout.removeWidget(self.viewcam1)

            # Create a new QDialog for fullscreen video
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")

            # Create a QVBoxLayout for the fullscreen dialog
            fullscreen_layout = QVBoxLayout()
            self.viewcam1_1 = self.viewcam1
            fullscreen_layout.addWidget(self.viewcam1_1)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)

            # Show the fullscreen dialog
            self.fullscreen_dialog.showFullScreen()

            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                # Close the fullscreen dialog
                self.fullscreen_dialog.close()
                self.viewcam1 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam1.setStyleSheet("background-color: rgb(170, 0, 0);")
                self.viewcam1.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam1.setScaledContents(True)
                self.viewcam1.setObjectName("viewcam1")
                self.gridLayout.addWidget(self.viewcam1, 4, 0, 1, 1)
                self.viewcam1.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam1.mousePressEvent = self.fullscreen_viewcam1

                # Re-add the widget to its original position
                # self.gridLayout.addWidget(self.viewcam1, self.saved_row, self.saved_col)

            self.is_fullscreen = False

    def fullscreen_viewcam2(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam2)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam2)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam2 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam2.setStyleSheet("background-color: rgb(0, 170, 0);")
                self.viewcam2.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam2.setScaledContents(True)
                self.viewcam2.setObjectName("viewcam2")
                self.gridLayout.addWidget(self.viewcam2, 4, 1, 1, 1)
                self.viewcam2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam2.mousePressEvent = self.fullscreen_viewcam2
            self.is_fullscreen = False
    def fullscreen_viewcam3(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam3)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam3)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam3 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam3.setStyleSheet("background-color: rgb(85, 170, 255);")
                self.viewcam3.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam3.setScaledContents(True)
                self.viewcam3.setObjectName("viewcam3")
                self.gridLayout.addWidget(self.viewcam3, 4, 2, 1, 1)
                self.viewcam3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam3.mousePressEvent = self.fullscreen_viewcam3
            self.is_fullscreen = False
    def fullscreen_viewcam4(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam4)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam4)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam4 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam4.setStyleSheet("background-color: rgb(170, 255, 255);")
                self.viewcam4.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam4.setScaledContents(True)
                self.viewcam4.setObjectName("viewcam4")
                self.gridLayout.addWidget(self.viewcam4, 5, 0, 1, 1)
                self.viewcam4.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam4.mousePressEvent = self.fullscreen_viewcam4
            self.is_fullscreen = False
    def fullscreen_viewcam5(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam5)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam5)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam5 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam5.setStyleSheet("background-color: rgb(255, 85, 127);")
                self.viewcam5.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam5.setScaledContents(True)
                self.viewcam5.setObjectName("viewcam5")
                self.gridLayout.addWidget(self.viewcam5, 5, 1, 1, 1)
                self.viewcam5.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam5.mousePressEvent = self.fullscreen_viewcam5
            self.is_fullscreen = False

    def fullscreen_viewcam6(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam6)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam6)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam6 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam6.setStyleSheet("background-color: rgb(255, 85, 0);")
                self.viewcam6.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam6.setScaledContents(True)
                self.viewcam6.setObjectName("viewcam6")
                self.gridLayout.addWidget(self.viewcam6, 5, 2, 1, 1)
                self.viewcam6.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam6.mousePressEvent = self.fullscreen_viewcam6
            self.is_fullscreen = False

    def fullscreen_viewcam7(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam7)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam7)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam7 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam7.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.viewcam7.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam7.setScaledContents(True)
                self.viewcam7.setObjectName("viewcam7")
                self.gridLayout.addWidget(self.viewcam7, 6, 0, 1, 1)
                self.viewcam7.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam7.mousePressEvent = self.fullscreen_viewcam7
            self.is_fullscreen = False

    def fullscreen_viewcam8(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam8)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam8)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam8 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam8.setStyleSheet("\n"
# "background-color: rgb(170, 170, 0);")
                self.viewcam8.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam8.setScaledContents(True)
                self.viewcam8.setObjectName("viewcam8")
                self.gridLayout.addWidget(self.viewcam8, 6, 1, 1, 1)
                self.viewcam8.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam8.mousePressEvent = self.fullscreen_viewcam8
            self.is_fullscreen = False

    def fullscreen_viewcam9(self, event):
        if not self.is_fullscreen:
            self.gridLayout.removeWidget(self.viewcam9)
            self.fullscreen_dialog = QDialog()
            self.fullscreen_dialog.setWindowTitle("Fullscreen Video")
            fullscreen_layout = QVBoxLayout()
            fullscreen_layout.addWidget(self.viewcam9)  # Add the video QLabel to the layout
            self.fullscreen_dialog.setLayout(fullscreen_layout)
            self.fullscreen_dialog.showFullScreen()
            self.is_fullscreen = True
        else:
            if self.fullscreen_dialog is not None:
                self.fullscreen_dialog.close()
                self.viewcam9 = QtWidgets.QLabel(self.Dialog)
                # self.viewcam9.setStyleSheet("background-color: rgb(170, 255, 127);")
                self.viewcam9.setFrameShape(QtWidgets.QFrame.Box)
                self.viewcam9.setFrameShadow(QtWidgets.QFrame.Plain)
                self.viewcam9.setLineWidth(1)
                self.viewcam9.setScaledContents(True)
                self.viewcam9.setObjectName("viewcam9")
                self.gridLayout.addWidget(self.viewcam9, 6, 2, 1, 1)
                self.viewcam9.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
                self.viewcam9.mousePressEvent = self.fullscreen_viewcam9
            self.is_fullscreen = False

    def select_combobox(self):
        selected_item = self.combobox_list.currentText()
        # self.label_2.setText(f"Bạn đã chọn: {selected_item}")
        print("Bạn đã chọn: " + selected_item)
        self.comboBox.clear()
        # db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
        #                      host='192.168.1.89', database='vehicle-identification')
        # cursor = db.cursor(buffered=True)
        ID_list_ = None
        sql2 = "SELECT id FROM listsvehicle WHERE name = %s"
        cursor.execute(sql2, (selected_item,))
        ID_list_ = cursor.fetchall()
        for ID_list in ID_list_:
            ID_list = ID_list[0]
            
            ID_camera = None
            sql5 = "SELECT camera_id FROM cameradetail WHERE list_vehicle_id = %s"
            cursor.execute(sql5, (ID_list,))
            ID_camera_ = cursor.fetchall()
            for ID_camera in ID_camera_:
                ID_camera = ID_camera[0]
                # cursor = db.cursor(buffered=True)
                sql3 = "SELECT rtsp FROM cameras WHERE id = %s"
                cursor.execute(sql3, (ID_camera,))
                results = cursor.fetchall()

                for result in results:
                    self.comboBox.addItem(result[0])
        
        # Xóa dữ liệu cũ từ QComboBox
        # self.comboBox_listxe.clear()

        # Thêm dữ liệu từ cơ sở dữ liệu vào QComboBox
        # for result in results:
        #     self.comboBox.addItem(result[0])

    def select_combobox_RTSP(self):
        selected_item = self.comboBox.currentText()
        # self.label_2.setText(f"Bạn đã chọn: {selected_item}")
        print("Bạn đã chọn: " + selected_item)
        return selected_item
    def button_f(self):
        # self.label_2.setText("nhan button file")
        print("nhan button file")
        global ui
        ui = formlist.main()
        self.closeEvent()
        MainWindow.close()


    def button_camera(self):
        # self.label_2.setText("nhan button camera")
        print("nhan button camera")
        self.stop_capture_video()
        self.start_capture_video()
    def button_setting(self):
        # self.label_2.setText("nhan button setting")
        print("nhan button setting")
        global ui
        ui = ADD.main()
        self.closeEvent()
        MainWindow.close()
    def comboBox_list_current(self):
        selected_item = self.combobox_list.currentText()
        return selected_item
    def button_bc(self):
        # self.label_2.setText("nhan button baocao")
        print("nhan button baocao")
        global ui
        ui = report_window.main()
        self.closeEvent()
        MainWindow.close()

    def button_LPR(self):
        global detect 
        detect = not detect
        # self.label_2.setText("nhan button reco")
        # global ui
        # ui = form_reco.main()
        # self.closeEvent()
        # MainWindow.close()
        print("nhan button reco")
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # hình sau khi convert từ CV 2 về hình ảnh hiện lên qt
        p = convert_to_Qt_format.scaled(1280 , 720, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)    
        
    def closeEvent(self):
        self.stop_capture_video()
    def stop_capture_video(self):
        self.thread[1].signal.disconnect(self.show_webcam1)
        self.thread[1].stop()
        # self.thread[2].stop()
        # self.thread[3].stop()
        # self.thread[4].stop()
    def show_webcam1(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam1.setPixmap(qt_frame)
    def show_webcam2(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam2.setPixmap(qt_frame)
    def show_webcam3(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam3.setPixmap(qt_frame)
    def show_webcam4(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam4.setPixmap(qt_frame)
    def show_webcam5(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam5.setPixmap(qt_frame)

    def show_webcam6(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam6.setPixmap(qt_frame)
    def show_webcam7(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam7.setPixmap(qt_frame)
    
    def show_webcam8(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam8.setPixmap(qt_frame)
    def show_webcam9(self, frame):
        qt_frame =self.convert_cv_qt(frame)
        self.viewcam9.setPixmap(qt_frame)
    def start_capture_video(self):
        self.thread[1] = capture_video(index = 1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_webcam1)

        # self.thread[2] = RTSP1(index= 2)
        # self.thread[2].start()
        # self.thread[2].signal1.connect(self.show_webcam2)   # signal nhận được hình ở luồng 2, sẽ gửi đến show_webcam

        # self.thread[3] = RTSP2(index= 3)
        # self.thread[3].start()
        # self.thread[3].signal2.connect(self.show_webcam3)

        # self.thread[4] = RTSP3(index= 4)
        # self.thread[4].start()
        # self.thread[4].signal3.connect(self.show_webcam4)

        # self.thread[5] = RTSP4(index= 5)
        # self.thread[5].start()
        # self.thread[5].signal4.connect(self.show_webcam5)

        # self.thread[6] = capture_video(index= 6)
        # self.thread[6].start()
        # self.thread[6].signal5.connect(self.show_webcam6)

        # self.thread[7] = capture_video(index= 7)
        # self.thread[7].start()
        # self.thread[7].signal6.connect(self.show_webcam7)

        # self.thread[8] = capture_video(index= 8)
        # self.thread[8].start()
        # self.thread[8].signal7.connect(self.show_webcam8)

        # self.thread[9] = capture_video(index= 9)
        # self.thread[9].start()
        # self.thread[9].signal8.connect(self.show_webcam9)
value_LP1 = None
value_feature = 1
image_directory = 'image_mysql'

class capture_video(QThread):
    global detect,ui,value_LP1,value_feature,image_directory,cursor,dbsql
    signal = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,


    def __init__(self, index):
        self.index = index         # index = 1 -> capture_video là luồng 1
        print("Start threading : ", self.index)
        super(capture_video, self).__init__()   # thừa hưởng , tái khẳng định

    def run(self):
        rtsp = Ui_MainWindow.select_combobox_RTSP(ui)
        print("rtsp: ", rtsp)
        if rtsp == "0":
            rtsp = 0
        cap = cv2.VideoCapture(rtsp)

        if cap.isOpened():
            frame_count = 0
            delay_frames = 6
            t1 = time.time()
            while True:
                ret, frame = cap.read()
                frame_count += 1
                if frame_count % delay_frames == 0:
                    if ret:
                        if detect:
                            frame,value_LP1 = main_image.detect_APP(weights_detect,weights_reco,frame)
                            print("Detect finished : " + str(value_LP1))
                            if value_LP1 != None:
                                # db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                                # host='192.168.1.89', database='vehicle-identification')
                                # cursor = db.cursor(buffered=True)
                                id_LP = None
                                cursor.execute("SELECT id FROM vehicles WHERE license_plate = %s", (value_LP1,))
                                id_LP = cursor.fetchone()
                                if id_LP is not None:
                                    id_LP = id_LP[0]
                                # cursor = db.cursor(buffered=True)
                                    vehicle_id = 0
                                    time_from_database = datetime.now()
                                    # Truy vấn SQL để lấy dòng mới nhất từ bảng
                                    query = "SELECT vehicle_id, time FROM records ORDER BY time DESC LIMIT 1"
                                    cursor.execute(query)
                                    row = cursor.fetchone()
                                    if row:
                                        # Trích xuất vehicle_id và time từ dòng kết quả
                                        vehicle_id, time_from_database = row

                                    if id_LP != vehicle_id:
                                        # id_LP = id_LP[0]
                                        rtsp = "0"
                                        id_rtsp = 0
                                        cursor.execute("SELECT id FROM cameras WHERE rtsp = %s", (rtsp,))
                                        id_rt = cursor.fetchone()
                                        id_rtsp = id_rt[0]
                                        # id_list_vehicle = 0
                                        # cursor.execute("SELECT list_vehicle_id FROM cameradetail WHERE camera_id = %s", (id_rtsp,))
                                        # id_list_ = cursor.fetchone()
                                        # id_list_vehicle = id_list_[0]

                                        name_list_vehicle = Ui_MainWindow.comboBox_list_current(ui)
                                        id_list_vehicle = 0
                                        cursor.execute("SELECT id FROM listsvehicle WHERE name = %s", (name_list_vehicle,))
                                        id_list_ = cursor.fetchone()
                                        id_list_vehicle = id_list_[0]
                                        to = time.time()
                                        dt = datetime.fromtimestamp(to)
                                        # Tạo một đối tượng timezone cho múi giờ MySQL (VD: múi giờ UTC)
                                        mysql_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

                                        # Chuyển đổi đối tượng datetime thành múi giờ MySQL
                                        dt_mysql = dt.astimezone(mysql_timezone)

                                        # Định dạng thời gian theo chuẩn MySQL (YYYY-MM-DD HH:MM:SS)
                                        formatted_time = dt_mysql.strftime("%Y-%m-%d %H:%M:%S")
                                        id_feature = None
                                        cursor.execute("SELECT id FROM features WHERE name = %s", (value_feature,))
                                        id_feature_ = cursor.fetchone()
                                        id_feature = id_feature_[0]
                                        image_filename = f"{uuid.uuid4()}-{int(time.time())}.jpg"
                                        path = os.path.join(image_directory, image_filename)
                                        if not os.path.exists(image_directory):
                                            os.makedirs(image_directory)    
                                        cv2.imwrite(path, frame)
                                        # sql = "INSERT INTO records (camera_id,list_vehicle_id,vehicle_id,feature_id,time,path) VALUES (%s,%s,%s,%s,%s,%s)"
                                        insert_query = """
                                        INSERT INTO records (camera_id, list_vehicle_id, vehicle_id, time, path)
                                        VALUES (%s, %s, %s, %s, %s)
                                        """
                                        values = (id_rtsp, id_list_vehicle, id_LP, formatted_time, path)
                                        # values = (id_rtsp,id_list_vehicle,id_LP,id_feature,formatted_time,path)
                                        cursor.execute(insert_query, values)
                                        dbsql.commit()

                                        record_id = None
                                        cursor.execute("SELECT id FROM records WHERE camera_id = %s AND list_vehicle_id = %s AND vehicle_id = %s AND path = %s", (id_rtsp, id_list_vehicle, id_LP, path))
                                        record_id_ = cursor.fetchone()
                                        record_id = record_id_[0]
                                        
                                        insert_query_reportdetail = """
                                        INSERT INTO recorddetail (feature_id,record_id)
                                        VALUES (%s, %s)
                                        """
                                        values = (id_feature, record_id)
                                        # values = (id_rtsp,id_list_vehicle,id_LP,id_feature,formatted_time,path)
                                        cursor.execute(insert_query_reportdetail, values)
                                        dbsql.commit()

                                    else:
                                        current_time = datetime.now()
                                        time_difference = current_time - time_from_database
                                        if time_difference > timedelta(seconds=60):
                                            rtsp = "0"
                                            id_rtsp = 0
                                            cursor.execute("SELECT id FROM cameras WHERE rtsp = %s", (rtsp,))
                                            id_rt = cursor.fetchone()
                                            id_rtsp = id_rt[0]
                                            # id_list_vehicle = 0
                                            # cursor.execute("SELECT list_vehicle_id FROM cameradetail WHERE camera_id = %s", (id_rtsp,))
                                            # id_list_ = cursor.fetchone()
                                            # id_list_vehicle = id_list_[0]

                                            name_list_vehicle = Ui_MainWindow.comboBox_list_current(ui)
                                            id_list_vehicle = 0
                                            cursor.execute("SELECT id FROM listsvehicle WHERE name = %s", (name_list_vehicle,))
                                            id_list_ = cursor.fetchone()
                                            id_list_vehicle = id_list_[0]
                                            to = time.time()
                                            dt = datetime.fromtimestamp(to)
                                            # Tạo một đối tượng timezone cho múi giờ MySQL (VD: múi giờ UTC)
                                            mysql_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

                                            # Chuyển đổi đối tượng datetime thành múi giờ MySQL
                                            dt_mysql = dt.astimezone(mysql_timezone)

                                            # Định dạng thời gian theo chuẩn MySQL (YYYY-MM-DD HH:MM:SS)
                                            formatted_time = dt_mysql.strftime("%Y-%m-%d %H:%M:%S")
                                            id_feature = None
                                            cursor.execute("SELECT id FROM features WHERE name = %s", (value_feature,))
                                            id_feature_ = cursor.fetchone()
                                            id_feature = id_feature_[0]
                                            image_filename = f"{uuid.uuid4()}-{int(time.time())}.jpg"
                                            path = os.path.join(image_directory, image_filename)
                                            if not os.path.exists(image_directory):
                                                os.makedirs(image_directory)    
                                            cv2.imwrite(path, frame)
                                            # sql = "INSERT INTO records (camera_id,list_vehicle_id,vehicle_id,feature_id,time,path) VALUES (%s,%s,%s,%s,%s,%s)"
                                            insert_query = """
                                            INSERT INTO records (camera_id, list_vehicle_id, vehicle_id, time, path)
                                            VALUES (%s, %s, %s, %s, %s)
                                            """
                                            values = (id_rtsp, id_list_vehicle, id_LP, formatted_time, path,)
                                            # values = (id_rtsp,id_list_vehicle,id_LP,id_feature,formatted_time,path)
                                            cursor.execute(insert_query, values)
                                            dbsql.commit()
                                            record_id = None
                                            cursor.execute("SELECT id FROM records WHERE camera_id = %s AND list_vehicle_id = %s AND vehicle_id = %s AND path = %s", (id_rtsp, id_list_vehicle, id_LP, path))
                                            record_id_ = cursor.fetchone()
                                            record_id = record_id_[0]
                                            
                                            insert_query_reportdetail = """
                                            INSERT INTO recorddetail (feature_id,record_id)
                                            VALUES (%s, %s)
                                            """
                                            values = (id_feature, record_id)
                                            # values = (id_rtsp,id_list_vehicle,id_LP,id_feature,formatted_time,path)
                                            cursor.execute(insert_query_reportdetail, values)
                                            dbsql.commit()

                        self.signal.emit(frame)     # suất tín hiệu gửi đi dạng frame, dùng emit để xuất đi
                    else:
                        break
        else :
            # self.stop()
            pass
    def stop(self):
        print("Stop threading : ", self.index)
        self.terminate()
class RTSP1(QThread):
    signal1 = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,
    def __init__(self, index):
        self.index = index         # index = 1 -> capture_video là luồng 1
        print("Start threading : ", self.index)
        super(RTSP1, self).__init__()   # thừa hưởng , tái khẳng định
    def run(self):
        path = 'rtsp://admin:Aipt123456>@192.168.1.59:554/1'
        cap = cv2.VideoCapture(path)
        frame_count = 0
        delay_frames = 1
        while True:
            ret, frame = cap.read()
            frame_count += 1
            if frame_count % delay_frames == 0:
                if ret:
                    self.signal1.emit(frame)     # suất tín hiệu gửi đi dạng frame, dùng emit để xuất đi
                else:
                    break
    def stop(self):
        print("Stop threading : ", self.index)
        self.terminate() 
class RTSP2(QThread):
    signal2 = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,
    def __init__(self, index):
        self.index = index         # index = 1 -> capture_video là luồng 1
        print("Start threading : ", self.index)
        super(RTSP2, self).__init__()   # thừa hưởng , tái khẳng định
    def run(self):
        path = 'rtsp://admin:aipt2023@192.168.1.56:554/1'
        cap = cv2.VideoCapture(path)
        frame_count = 0
        delay_frames = 1
        while True:
            ret, frame = cap.read()
            frame_count += 1
            if frame_count % delay_frames == 0:
                if ret:
                    self.signal2.emit(frame)     # suất tín hiệu gửi đi dạng frame, dùng emit để xuất đi
                else:
                    break
    def stop(self):
        print("Stop threading : ", self.index)
        self.terminate()
class RTSP3(QThread):
    signal3 = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,
    def __init__(self, index):
        self.index = index         # index = 1 -> capture_video là luồng 1
        print("Start threading : ", self.index)
        super(RTSP3, self).__init__()   # thừa hưởng , tái khẳng định

    def run(self):
        path = 'rtsp://admin:Aipt123456>@192.168.1.58:554/1'
        cap = cv2.VideoCapture(path)
        frame_count = 0
        delay_frames = 1
        while True:
            ret, frame = cap.read()
            frame_count += 1
            if frame_count % delay_frames == 0:
                if ret:
                    # frame = self.detect_APP(frame)
                    self.signal3.emit(frame)     # suất tín hiệu gửi đi dạng frame, dùng emit để xuất đi
                else:
                    break
    def stop(self):
        print("Stop threading : ", self.index)
        self.terminate()
class RTSP4(QThread):
    signal4 = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,
    def __init__(self, index):
        self.index = index         # index = 1 -> capture_video là luồng 1
        print("Start threading : ", self.index)
        super(RTSP4, self).__init__()   # thừa hưởng , tái khẳng định

    def run(self):
        path = r"E:\AIPT\APP_QT\detect_LPR\test_image\4.mp4"
        cap = cv2.VideoCapture(path)
        frame_count = 0
        delay_frames = 1
        while True:
            ret, frame = cap.read()
            frame_count += 1
            if frame_count % delay_frames == 0:
                if ret:
                    # frame = self.detect_APP(frame)
                    self.signal4.emit(frame)     # suất tín hiệu gửi đi dạng frame, dùng emit để xuất đi
                else:
                    break
    def stop(self):
        print("Stop threading : ", self.index)
        self.terminate()
import test_rc


def main():
    global ui
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

if __name__ == "__main__":
    main()
    sys.exit(app.exec_())
