from PyQt5.QtWidgets import  QDialog, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
# import LPR.main_image as main_image
import form_reco as form_reco
import os
import logging
import Setup_main as Setup_main
from PyQt5.QtWidgets import  QMainWindow

current_directory = os.getcwd()
pathlog = current_directory + '/myapp.log'
logging.basicConfig(filename=pathlog, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
vehicle_company_id = 1

# app = QApplication(sys.argv)
MainWindow = QMainWindow()
# ui = ''
detect= False
tetail_cam1 =[]
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # global ui
        # self.showFullScreen()
        self.thread = {}
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(968, 657)
        # MainWindow.showMaximized()
        # MainWindow.showfullscreen()
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
        self.Buttoncam = QtWidgets.QPushButton(self.centralwidget)
        self.Buttoncam.setMaximumSize(QtCore.QSize(60, 50))
        self.Buttoncam.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"image: url(:/newPrefix/image/camera.png);")
        self.Buttoncam.setText("")
        self.Buttoncam.setObjectName("Buttoncam")
        self.horizontalLayout.addWidget(self.Buttoncam)
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
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.Button_baocao = QtWidgets.QPushButton(self.centralwidget)
        self.Button_baocao.setMaximumSize(QtCore.QSize(60, 50))
        self.Button_baocao.setStyleSheet("background-color: rgb(85, 255, 255);\n"
"image: url(:/newPrefix/image/menu.png);")
        self.Button_baocao.setText("")
        self.Button_baocao.setObjectName("Button_baocao")
        self.horizontalLayout.addWidget(self.Button_baocao)
        self.Button_Reco = QtWidgets.QPushButton(self.centralwidget)
        self.Button_Reco.setMaximumSize(QtCore.QSize(60, 50))
        self.Button_Reco.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"image: url(:/newPrefix/image/car.png);")
        self.Button_Reco.setText("")
        self.Button_Reco.setObjectName("Button_Reco")
        self.horizontalLayout.addWidget(self.Button_Reco)
        self.Button_setting = QtWidgets.QPushButton(self.centralwidget)
        self.Button_setting.setMaximumSize(QtCore.QSize(60, 50))
        self.Button_setting.setStyleSheet("background-color: rgb(170, 255, 255);\n"
"image: url(:/newPrefix/image/settings.png);")
        self.Button_setting.setText("")
        self.Button_setting.setObjectName("Button_setting")
        self.horizontalLayout.addWidget(self.Button_setting)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(7)
        self.gridLayout.setObjectName("gridLayout")
        self.viewcam3 = QtWidgets.QLabel(self.centralwidget)
        self.viewcam3.setFrameShape(QtWidgets.QFrame.Box)
        self.viewcam3.setScaledContents(True)
        self.viewcam3.setObjectName("viewcam3")
        self.gridLayout.addWidget(self.viewcam3, 4, 2, 1, 1)


        self.viewcam1 = QtWidgets.QLabel(self.centralwidget)
        # self.viewcam1 = Setup_main1.VideoDisplay()
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
        # try:
        #     self.start_capture_video()
        # except Exception as e:
        #     # Ghi lại lỗi nếu có
        #     logging.error("243 error :  %s", str(e))
        # RTSP_main.load_data_to_combobox_list_and_rtsp(self.combobox_list)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    
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
                # self.viewcam1 = Setup_main1.VideoDisplay()
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

import test_rc
