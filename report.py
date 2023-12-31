from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel,QDateTime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import main as main_Window
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import os
import sql as aiptsql
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui=''
current_directory = os.getcwd()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global ui,current_directory

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1394, 753)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(6, 3, 3, 3)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMaximumSize(QtCore.QSize(250, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)


        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(250, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)


        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMaximumSize(QtCore.QSize(250, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)


        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QtCore.QSize(250, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)


        self.textEdit_bienso = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_bienso.sizePolicy().hasHeightForWidth())
        self.textEdit_bienso.setSizePolicy(sizePolicy)
        self.textEdit_bienso.setMaximumSize(QtCore.QSize(230, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.textEdit_bienso.setFont(font)
        self.textEdit_bienso.setObjectName("textEdit_bienso")


        self.gridLayout.addWidget(self.textEdit_bienso, 1, 1, 1, 1)
        self.dateTimeEdit_start = QtWidgets.QDateTimeEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateTimeEdit_start.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit_start.setSizePolicy(sizePolicy)
        self.dateTimeEdit_start.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.dateTimeEdit_start.setFont(font)
        self.dateTimeEdit_start.setObjectName("dateTimeEdit_start")
        self.gridLayout.addWidget(self.dateTimeEdit_start, 3, 0, 1, 1)
        new_date_time_start = QDateTime.currentDateTime()  # Lấy thời gian hiện tại
        self.dateTimeEdit_start.setDateTime(new_date_time_start)  # Thiết lập giá trị cho QDateTimeEdit
        
        
        self.comboBox_nhan_videocamera = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_nhan_videocamera.sizePolicy().hasHeightForWidth())
        self.comboBox_nhan_videocamera.setSizePolicy(sizePolicy)
        self.comboBox_nhan_videocamera.setMaximumSize(QtCore.QSize(230, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.comboBox_nhan_videocamera.setFont(font)
        self.comboBox_nhan_videocamera.addItem("")
        self.comboBox_nhan_videocamera.setObjectName("comboBox_nhan_videocamera")
        self.gridLayout.addWidget(self.comboBox_nhan_videocamera, 1, 0, 1, 1)
        self.comboBox_nhan_videocamera.currentIndexChanged.connect(self.select_combobox)



        self.dateTimeEdit_end = QtWidgets.QDateTimeEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateTimeEdit_end.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit_end.setSizePolicy(sizePolicy)
        self.dateTimeEdit_end.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.dateTimeEdit_end.setFont(font)
        self.dateTimeEdit_end.setObjectName("dateTimeEdit_end")
        self.gridLayout.addWidget(self.dateTimeEdit_end, 3, 1, 1, 1)
		# new_date_time = QDateTime.currentDateTime()  # Lấy thời gian hiện tại
        self.dateTimeEdit_end.setDateTime(new_date_time_start)  # Thiết lập giá trị cho QDateTimeEdit
        # self.comboBox_nhan_videocamera.addItem("Tat ca")

        self.verticalLayout_2.addLayout(self.gridLayout)
        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setMaximumSize(QtCore.QSize(500, 16777215))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.verticalLayout_2.addWidget(self.line_11)


        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_thongtintimkiem = QtWidgets.QLabel(self.centralwidget)
        self.label_thongtintimkiem.setText("")
        self.label_thongtintimkiem.setObjectName("label_thongtintimkiem")
        self.verticalLayout_3.addWidget(self.label_thongtintimkiem)


        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMaximumSize(QtCore.QSize(500, 60))
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)


        self.checkBox_bienso = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_bienso.setMaximumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_bienso.setFont(font)
        self.checkBox_bienso.setObjectName("checkBox_bienso")
        self.horizontalLayout_5.addWidget(self.checkBox_bienso)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.checkBox_nhanxe = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_nhanxe.setMaximumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_nhanxe.setFont(font)
        self.checkBox_nhanxe.setObjectName("checkBox_nhanxe")
        
        self.horizontalLayout_4.addWidget(self.checkBox_nhanxe)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)


        self.checkBox_mauxe = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_mauxe.setMaximumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_mauxe.setFont(font)
        self.checkBox_mauxe.setObjectName("checkBox_mauxe")
        self.horizontalLayout_3.addWidget(self.checkBox_mauxe)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_6.addWidget(self.label_12)


        self.checkBox_soluongxe = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_soluongxe.setMaximumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_soluongxe.setFont(font)
        self.checkBox_soluongxe.setObjectName("checkBox_soluongxe")
        self.horizontalLayout_6.addWidget(self.checkBox_soluongxe)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Button_timkiem = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_timkiem.sizePolicy().hasHeightForWidth())
        self.Button_timkiem.setSizePolicy(sizePolicy)
        self.Button_timkiem.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Button_timkiem.setFont(font)
        self.Button_timkiem.setStyleSheet("image: url(:/newPrefix/image/magnifying.png);\n"
"background-color: rgb(255, 255, 255);")
        self.Button_timkiem.setText("")
        icon = QtGui.QIcon.fromTheme("Tìmkiếm")
        self.Button_timkiem.setIcon(icon)
        self.Button_timkiem.setIconSize(QtCore.QSize(30, 30))
        self.Button_timkiem.setDefault(True)
        self.Button_timkiem.setObjectName("Button_timkiem")
        self.horizontalLayout_2.addWidget(self.Button_timkiem)
        self.Button_timkiem.clicked.connect(self.timkiem)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Button_xoa = QtWidgets.QPushButton(self.centralwidget)
        self.Button_xoa.setMaximumSize(QtCore.QSize(140, 60))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_xoa.setFont(font)
        self.Button_xoa.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/newPrefix/image/remove.png);")
        self.Button_xoa.setDefault(True)
        self.Button_xoa.setObjectName("Button_xoa")
        self.gridLayout_2.addWidget(self.Button_xoa, 1, 0, 1, 1)
        self.Button_xoa.clicked.connect(self.delete_selected_row)


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)


        self.Button_mainw = QtWidgets.QPushButton(self.centralwidget)
        self.Button_mainw.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Button_mainw.setFont(font)
        self.Button_mainw.setObjectName("Button_mainw")
        self.gridLayout_2.addWidget(self.Button_mainw, 1, 3, 1, 1, QtCore.Qt.AlignRight)
        self.Button_mainw.clicked.connect(self.button_mainw)
        self.label_tongso = QtWidgets.QLabel(self.centralwidget)
        self.label_tongso.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_tongso.setObjectName("label_tongso")
        self.gridLayout_2.addWidget(self.label_tongso, 1, 2, 1, 1)


        self.label_report = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_report.sizePolicy().hasHeightForWidth())
        self.label_report.setSizePolicy(sizePolicy)
        self.label_report.setMaximumSize(QtCore.QSize(16777215, 60))
        self.label_report.setText("")
        self.label_report.setObjectName("label_report")
        self.gridLayout_2.addWidget(self.label_report, 0, 0, 1, 4)


        self.Tableview = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Tableview.setFont(font)
        self.Tableview.setAutoFillBackground(True)
        self.Tableview.setAutoScrollMargin(18)
        self.Tableview.setColumnCount(6)
        self.Tableview.setObjectName("Tableview")
        self.Tableview.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.Tableview.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Tableview.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Tableview.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Tableview.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Tableview.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.Tableview.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        font.setItalic(False)
        item.setFont(font)
        self.Tableview.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.Tableview.setItem(1, 5, item)
        self.Tableview.horizontalHeader().setCascadingSectionResizes(True)
        self.Tableview.horizontalHeader().setDefaultSectionSize(237)
        self.Tableview.horizontalHeader().setMinimumSectionSize(96)
        self.Tableview.horizontalHeader().setSortIndicatorShown(True)
        self.Tableview.horizontalHeader().setStretchLastSection(False)
        self.Tableview.verticalHeader().setCascadingSectionResizes(False)
        self.Tableview.verticalHeader().setMinimumSectionSize(27)
        self.Tableview.verticalHeader().setSortIndicatorShown(False)
        self.Tableview.verticalHeader().setStretchLastSection(False)
        self.gridLayout_2.addWidget(self.Tableview, 5, 0, 1, 4)
        self.Tableview.horizontalHeader().sectionClicked.connect(self.handle_column_header_clicked)
        self.Tableview.verticalHeader().sectionClicked.connect(self.handle_row_header_clicked)
        self.Tableview.cellClicked.connect(self.handle_cell_clicked)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        
        

        # pixmap1 = QPixmap(r'E:\AIPT\APP_QT\detect_LPR\test_image\1.jpg')
        # pixmap1 = pixmap1.scaledToWidth(240)
        # pixmap1 = pixmap1.scaledToHeight(200)
        # item1 = QTableWidgetItem()
        # item1.setData(Qt.DecorationRole, pixmap1)
        # self.Tableview.setItem(2, 2, item1)

        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.load_data()
        # self.default_setup()
        self.Tableview.resizeColumnsToContents()
        self.Tableview.resizeRowsToContents()
        # Thiết lập kích thước mặc định cho hàng và cột
        for row in range(self.Tableview.rowCount()):
            self.Tableview.setRowHeight(row, 200)  # Đặt chiều cao hàng là 200
        for col in range(self.Tableview.columnCount()):
            self.Tableview.setColumnWidth(col, 240)  # Đặt chiều rộng cột là 240

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Report"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Báo cáo kết quả nhận diện</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Biển số xe</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Nhãn Video/Camera</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Thời gian bắt đầu</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Thời gian kết thúc</span></p></body></html>"))
        self.comboBox_nhan_videocamera.setItemText(0, _translate("MainWindow", "Tat ca"))
        # self.comboBox_nhan_videocamera.setItemText(0, _translate("MainWindow", "New Item"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Các đặc điểm nhận diện</span></p></body></html>"))
        self.checkBox_bienso.setText(_translate("MainWindow", "Phát hiện biển số xe"))
        self.checkBox_nhanxe.setText(_translate("MainWindow", "Phát hiện nhãn hiệu xe"))
        self.checkBox_mauxe.setText(_translate("MainWindow", "Phát hiện màu xe"))
        self.checkBox_soluongxe.setText(_translate("MainWindow", "Phát hiện số lượng xe"))
        self.Button_xoa.setText(_translate("MainWindow", "               Xóa"))
        self.Button_mainw.setText(_translate("MainWindow", "Quay Lại"))
        self.label_tongso.setText(_translate("MainWindow", "TỔNG SỐ : "))
        self.Tableview.setSortingEnabled(True)
      
        item = self.Tableview.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Biển số xe/đặc điểm"))
        item = self.Tableview.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Thời gian phát hiện"))
        item = self.Tableview.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Danh sách phát hiện"))
        item = self.Tableview.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Nhãn video/Camera"))
        item = self.Tableview.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Bản ghi lưu trữ"))
        item = self.Tableview.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Ảnh"))
        __sortingEnabled = self.Tableview.isSortingEnabled()
        self.Tableview.setSortingEnabled(False)
        self.Tableview.setSortingEnabled(__sortingEnabled)


    def show_tableview(self,row_index,row):
        id,camera_id, list_vehicle_id, vehicle_id, time, path = row
        license_plate = aiptsql.fetch_vehicle_info(vehicle_id)
        self.Tableview.setItem(row_index, 0, QTableWidgetItem(str(license_plate)))

        self.Tableview.setItem(row_index, 1, QTableWidgetItem(str(time)))

        list_vehicle_ = aiptsql.fetch_list_vehicle_info(list_vehicle_id)
        self.Tableview.setItem(row_index, 2 , QTableWidgetItem(str(list_vehicle_)))

        rtsp = aiptsql.fetch_camera_info(camera_id)
        self.Tableview.setItem(row_index, 3 , QTableWidgetItem(str(rtsp)))

        self.Tableview.setItem(row_index, 4, QTableWidgetItem(path))
        path = current_directory + "\\" + str(path)
        print("path : " + path)

        pixmap1 = QPixmap(path)
        pixmap1 = pixmap1.scaledToWidth(240)
        pixmap1 = pixmap1.scaledToHeight(200)
        item1 = QTableWidgetItem()
        item1.setData(Qt.DecorationRole, pixmap1)
        self.Tableview.setItem(row_index, 5, item1)

    def load_data(self):
        global current_directory
        results = aiptsql.get_list_and_rtsp()
        for result in results:
            self.comboBox_nhan_videocamera.addItem(result)
        data = aiptsql.fetch_data()
        if data:
            self.Tableview.setRowCount(len(data))
            self.Tableview.setColumnCount(len(data[0]))
            for row_index, row in enumerate(data):
                self.show_tableview(row_index,row)

    def default_setup(self):
        self.Tableview.resizeColumnsToContents()
        self.Tableview.resizeRowsToContents()
        for row in range(self.Tableview.rowCount()):
            self.Tableview.setRowHeight(row, 200)  # Đặt chiều cao hàng là 200
        for col in range(self.Tableview.columnCount()):
            self.Tableview.setColumnWidth(col, 240)  # Đặt chiều rộng cột là 240
        
    
    def select_combobox(self):
        selected_item = self.comboBox_nhan_videocamera.currentText()
        rtsp = None
        if selected_item != "Tat ca":
            parts = selected_item.split("/")
            if len(parts) == 2:
                name_list = parts[0]
                rtsp = parts[1]

                while self.Tableview.rowCount() > 0:
                    self.Tableview.removeRow(0)
                camera_id_ = aiptsql.get_id_camera_where_rtsp(rtsp)
                row_table = 0
                for camera_id in camera_id_:
                    data =aiptsql.fetch_data_with_rtsp(camera_id[0])
                    if data:
                        self.Tableview.setColumnCount(len(data[0]))
                        
                        for row_index, row in enumerate(data):
                            self.Tableview.setRowCount(row_table + 1)
                            self.default_setup()
                            self.show_tableview(row_table, row)
                            row_table = row_table + 1 
        else :
            data = aiptsql.fetch_data()
            self.default_setup()
            if data:
                self.Tableview.setRowCount(len(data))
                self.Tableview.setColumnCount(len(data[0]))
                for row_index, row in enumerate(data):
                    self.default_setup()
                    self.show_tableview(row_index, row)


    def button_mainw(self):
        global ui
        ui = main_Window.main()
        MainWindow.close()
        
    def timkiem(self):
        is_checked_bienso = self.checkBox_bienso.isChecked()
        is_checked_nhanxe = self.checkBox_nhanxe.isChecked()
        is_checked_mauxe = self.checkBox_mauxe.isChecked()
        is_checked_soluongxe = self.checkBox_soluongxe.isChecked()
        while self.Tableview.rowCount() > 0:
            self.Tableview.removeRow(0)
        if is_checked_bienso:
             print("bien so is checked")
        else:
             print("bien so is unchecked")
        if is_checked_nhanxe:
            print("Nhan xe is checked")
        else:
            print("Nhan xe is unchecked")
        if is_checked_mauxe:
            print("Mau xe is checked")
        else:
            print("Mau xe is unchecked")
        if is_checked_soluongxe:
            print("Soluong xe is checked")
        else:
            print("Soluong xe is unchecked")
        date_time_start = self.dateTimeEdit_start.dateTime()
        date_time_start = date_time_start.toString("yyyy-MM-dd HH:mm:ss")
        print("Selected Date and Time start:", date_time_start)
        date_time_end = self.dateTimeEdit_end.dateTime()
        date_time_end = date_time_end.toString("yyyy-MM-dd HH:mm:ss")
        print("Selected Date and Time end:", date_time_end)
        selected_item = self.comboBox_nhan_videocamera.currentText()
        
        seach_selected = True
        if selected_item == "Tat ca":
            seach_selected = False
        else:
            parts = selected_item.split("/")
            if len(parts) == 2:
                name_list = parts[0]
                rtsp_item_combobox = parts[1]

        print("Selected Item:", selected_item)
        
        text_bienso = self.textEdit_bienso.toPlainText()
        
        if text_bienso and seach_selected == False:
            id_LP_ = aiptsql.get_id_vehicle_where_LP(text_bienso)
            row_table=0
            if id_LP_ :
                for id_LP in id_LP_:
                    if date_time_end == date_time_start:
                        data = aiptsql.fetch_data_with_id_LP(id_LP[0])
                        if data:
                            self.Tableview.setColumnCount(len(data[0]))
                            for row_index, row in enumerate(data):
                                self.Tableview.setRowCount(row_table + 1)
                                self.default_setup()
                                self.show_tableview(row_table, row)
                                row_table = row_table + 1 
                    else:
                        data = aiptsql.fetch_data_with_id_LP_and_time(id_LP[0],date_time_start,date_time_end)
                        if data:
                            self.Tableview.setColumnCount(len(data[0]))
                            for row_index, row in enumerate(data):
                                self.Tableview.setRowCount(row_table + 1)
                                self.default_setup()
                                self.show_tableview(row_table, row)
                                row_table = row_table + 1 
        elif text_bienso and seach_selected == True :
            rtsp_id_ = aiptsql.get_id_camera_where_rtsp(rtsp_item_combobox)
            for rtsp_id in rtsp_id_:
                rtsp_id = rtsp_id[0]
                id_LP_ = aiptsql.get_id_vehicle_where_LP(text_bienso)
                row_table=0
                if rtsp_id and id_LP_ :
                    for id_LP in id_LP_:
                        if date_time_start == date_time_end:
                            data = aiptsql.fetch_data_with_id_LP_and_list_vehicle(id_LP[0],rtsp_id)
                            if data:
                                self.Tableview.setColumnCount(len(data[0]))
                                for row_index, row in enumerate(data):
                                    self.Tableview.setRowCount(row_table + 1)
                                    self.default_setup()
                                    self.show_tableview(row_table, row)
                                    row_table = row_table + 1 
                        else:
                            data = aiptsql.fetch_data_with_id_LP_and_list_vehicle_and_time(id_LP[0],rtsp_id,date_time_start,date_time_end)
                            if data:
                                self.Tableview.setColumnCount(len(data[0]))
                                for row_index, row in enumerate(data):
                                    self.Tableview.setRowCount(row_table + 1)
                                    self.default_setup()
                                    self.show_tableview(row_table, row)
                                    row_table = row_table + 1
        elif text_bienso == "" and seach_selected == False:
            while self.Tableview.rowCount() > 0:
                self.Tableview.removeRow(0)
            data =aiptsql.fetch_data_with_time(date_time_start, date_time_end)
            row_table = 0
            if data:
                    self.Tableview.setColumnCount(len(data[0]))
                    
                    for row_index, row in enumerate(data):
                        self.Tableview.setRowCount(row_table + 1)
                        self.default_setup()
                        self.show_tableview(row_table, row)
                        row_table = row_table + 1    
        elif text_bienso == "" and seach_selected == True:
            parts = selected_item.split("/")
            if len(parts) == 2:
                name_list = parts[0]
                rtsp = parts[1]
            while self.Tableview.rowCount() > 0:
                self.Tableview.removeRow(0)
            camera_id_ = aiptsql.get_id_camera_where_rtsp(rtsp)
            row_table = 0
            for camera_id in camera_id_:
                data = aiptsql.fetch_data_with_rtsp_and_time(camera_id[0],date_time_start,date_time_end)
                if data:
                    self.Tableview.setColumnCount(len(data[0]))
                    for row_index, row in enumerate(data):
                        self.Tableview.setRowCount(row_table + 1)
                        self.default_setup()
                        self.show_tableview(row_table, row)
                        row_table = row_table + 1 
        self.label_tongso.setText("Tổng số " + str(self.Tableview.currentRow()))
        self.table_report()

    def table_report(self):
        print("table_report")

    def handle_cell_clicked(self, row, col):
        item = self.Tableview.item(row, col)
        if item:
                print(f"Cell ({row}, {col}) clicked, value: {item.text()}")
        else:
                print(f"Cell ({row}, {col}) clicked, no item")
    def handle_column_header_clicked(self, col):
        print(f'Column header clicked: {col}')

    def handle_row_header_clicked(self, row):
        print(f'Row header clicked: {row}')

    def delete_selected_row(self):
        selected_row = self.Tableview.currentRow()
        if selected_row >= 0:
            self.Tableview.removeRow(selected_row)

import test_rc
def main():
    global ui
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

if __name__ == "__main__":
    main()
    sys.exit(app.exec_())