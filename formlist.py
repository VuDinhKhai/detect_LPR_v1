# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fromlist1.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import main as main_Window
import sys
from PyQt5.QtWidgets import  QFileDialog
import mysql.connector

db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = ''
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global ui
        self.db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(3, 3, 3, 6)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.line_4.setFont(font)
        self.line_4.setStyleSheet("font: 75 8pt \"MS Shell Dlg 2\";")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)


        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.comboBox_list_link = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_list_link.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.comboBox_list_link.setFont(font)
        self.comboBox_list_link.setObjectName("comboBox_list_link")
        self.verticalLayout.addWidget(self.comboBox_list_link)
        self.comboBox_list_link.currentIndexChanged.connect(self.select_combobox)


        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_cha = QtWidgets.QLabel(self.centralwidget)
        self.label_cha.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_cha.setFont(font)
        self.label_cha.setStyleSheet("")
        self.label_cha.setObjectName("label_cha")
        self.horizontalLayout.addWidget(self.label_cha)


        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout.addWidget(self.line_5)


        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)


        self.comboBox_child = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_child.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.comboBox_child.setFont(font)
        self.comboBox_child.setObjectName("comboBox_child")
        self.verticalLayout_2.addWidget(self.comboBox_child)
        self.comboBox_child.currentIndexChanged.connect(self.select_combobox_child)


        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.text_edit_RTSP = QtWidgets.QTextEdit(self.centralwidget)
        self.text_edit_RTSP.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.text_edit_RTSP.setFont(font)
        self.text_edit_RTSP.setObjectName("text_edit_RTSP")
        self.verticalLayout.addWidget(self.text_edit_RTSP)


        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Button_luu_vitri = QtWidgets.QPushButton(self.centralwidget)
        self.Button_luu_vitri.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Button_luu_vitri.setFont(font)
        self.Button_luu_vitri.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.Button_luu_vitri.setDefault(True)
        self.Button_luu_vitri.setObjectName("Button_luu_vitri")
        self.horizontalLayout_2.addWidget(self.Button_luu_vitri)
        self.Button_luu_vitri.clicked.connect(self.luu_vitri)

        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_2.addWidget(self.line_6)
        self.Button_luu = QtWidgets.QPushButton(self.centralwidget)
        self.Button_luu.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Button_luu.setFont(font)
        self.Button_luu.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.Button_luu.setDefault(True)
        self.Button_luu.setObjectName("Button_luu")
        self.horizontalLayout_2.addWidget(self.Button_luu)
        self.Button_luu.clicked.connect(self.luu_RTSP)

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Button_xoa_vitri = QtWidgets.QPushButton(self.centralwidget)
        self.Button_xoa_vitri.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Button_xoa_vitri.setFont(font)
        self.Button_xoa_vitri.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.Button_xoa_vitri.setDefault(True)
        self.Button_xoa_vitri.setObjectName("Button_xoa_vitri")
        self.horizontalLayout_3.addWidget(self.Button_xoa_vitri)
        self.Button_xoa_vitri.clicked.connect(self.button_xoa_vitri)

        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_3.addWidget(self.line_7)


        self.Button_xoa = QtWidgets.QPushButton(self.centralwidget)
        self.Button_xoa.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Button_xoa.setFont(font)
        self.Button_xoa.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.Button_xoa.setDefault(True)
        self.Button_xoa.setObjectName("Button_xoa")
        self.horizontalLayout_3.addWidget(self.Button_xoa)
        self.Button_xoa.clicked.connect(self.button_xoa_RTSP)

        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.Button_mofile = QtWidgets.QPushButton(self.centralwidget)
        self.Button_mofile.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Button_mofile.setFont(font)
        self.Button_mofile.setStyleSheet("\n"
"background-color: rgb(216, 216, 216);")
        self.Button_mofile.setDefault(True)
        self.Button_mofile.setObjectName("Button_mofile")
        self.verticalLayout.addWidget(self.Button_mofile)
        self.Button_mofile.clicked.connect(self.openFile)

        self.Button_thoat = QtWidgets.QPushButton(self.centralwidget)
        self.Button_thoat.setMaximumSize(QtCore.QSize(9999999, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Button_thoat.setFont(font)
        self.Button_thoat.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.Button_thoat.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.Button_thoat.setDefault(True)
        self.Button_thoat.setObjectName("Button_thoat")
        self.verticalLayout.addWidget(self.Button_thoat)
        self.Button_thoat.clicked.connect(self.button_thoat)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # try:
        #     with open(r"E:\AIPT\APP_QT\detect_LPR\data_RTSP.txt", "r") as file:
        #         lines = file.readlines()
        #         for line in lines:
        #             self.comboBox_list_link.addItem(line.strip())
        # except FileNotFoundError:
        #     pass
        self.load_data_to_combobox()

        # self.comboBox_list_link.currentIndexChanged.connect(self.update_mysql_data)
        # self.comboBox_list_link.currentIndexChanged.connect(self.saveDataToFile)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Formlist"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">VỊ TRÍ CAMERA</p></body></html>"))
        self.label_cha.setText(_translate("MainWindow", "Cong A"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:400;\">Danh sách các luồng RTSP</span></p></body></html>"))
        self.Button_luu_vitri.setText(_translate("MainWindow", "LƯU VỊ TRÍ CAMERA"))
        self.Button_luu.setText(_translate("MainWindow", "LƯU RTSP"))
        self.Button_xoa_vitri.setText(_translate("MainWindow", "XÓA VỊ TRÍ CAMERA"))
        self.Button_xoa.setText(_translate("MainWindow", "XÓA RTSP"))
        self.Button_mofile.setText(_translate("MainWindow", "CHỌN TỆP"))
        self.Button_thoat.setText(_translate("MainWindow", "Quay Lại"))
    def load_data_to_combobox(self):
        self.db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM listsvehicle WHERE status = 1")

        for row in cursor.fetchall():
            self.comboBox_list_link.addItem(row[0])

        # cursor.execute("SELECT rtsp FROM cameras")
        # results = cursor.fetchall()

        # for result in results:
        #     self.comboBox_child.addItem(result[0])

        cursor.close()

    

    def select_combobox(self):
        selected_item = self.comboBox_list_link.currentText()
        self.comboBox_child.clear()
        db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        cursor = db.cursor(buffered=True)
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
                cursor = db.cursor(buffered=True)
                sql3 = "SELECT rtsp FROM cameras WHERE id = %s"
                cursor.execute(sql3, (ID_camera,))
                results = cursor.fetchall()

                for result in results:
                    self.comboBox_child.addItem(result[0])


        self.label_cha.setText(f"{selected_item}")

    def select_combobox_child(self):
        selected_item = self.comboBox_child.currentText()
        self.text_edit_RTSP.setText(f"{selected_item}")
    def button_thoat(self):
        # self.saveDataToFile()
        global ui
        ui = main_Window.main()
        MainWindow.close()
    def luu_vitri(self):
        db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        cursor = db.cursor()
        value = self.text_edit_RTSP.toPlainText()
        status = 1
        if len(value) !=0:
            found = True
            for index in range(self.comboBox_list_link.count()):
                item_text = self.comboBox_list_link.itemText(index)
                if item_text == value:
                    found = False
                    break
            if found:
                query = "SELECT * FROM listsvehicle WHERE name = %s"
                cursor.execute(query, (value,))
                existing_camera = cursor.fetchone()

                if existing_camera is None:
                    # Nếu rtsp chưa tồn tại, thêm một dòng mới vào bảng
                    insert_query = "INSERT INTO listsvehicle (name, status) VALUES (%s, %s)"
                    cursor.execute(insert_query, (value, status))
                    db.commit()
                    # print("Thêm mới thành công.")
                else:
                    # Nếu rtsp đã tồn tại, cập nhật trạng thái status từ 0 thành 1
                    update_query = "UPDATE listsvehicle SET status = 1 WHERE name = %s"
                    cursor.execute(update_query, (value,))
                    db.commit()
                    # print("Cập nhật thành công.")

                self.comboBox_list_link.addItem(value)
                self.label_cha.setText("Đã thêm : " + value)
        
    def luu_RTSP(self):
        db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        cursor = db.cursor()
        value = self.text_edit_RTSP.toPlainText()
        selected_item = self.comboBox_list_link.currentText()
        status = 1
        if len(value) !=0:
            found = True
            for index in range(self.comboBox_child.count()):
                item_text = self.comboBox_child.itemText(index)
                if item_text == value:
                    found = False
                    break
            if found:            
                self.comboBox_child.addItem(value)
                self.text_edit_RTSP.setText(value)
                query = "SELECT * FROM cameras WHERE rtsp = %s"
                cursor.execute(query, (value,))
                existing_camera = cursor.fetchone()

                if existing_camera is None:
                    # Nếu rtsp chưa tồn tại, thêm một dòng mới vào bảng
                    insert_query = "INSERT INTO cameras (name,rtsp, status) VALUES (%s, %s,%s)"
                    cursor.execute(insert_query, (selected_item,value, status))
                    db.commit()
                else:
                    # Nếu rtsp đã tồn tại, cập nhật trạng thái status từ 0 thành 1
                    update_query = "UPDATE cameras SET status = 1 WHERE rtsp = %s"
                    cursor.execute(update_query, (value,))
                    db.commit()


                # sql = "INSERT INTO cameras (name,rtsp,status) VALUES (%s,%s,%s)"
                # values = (selected_item,value,status,)
                # cursor.execute(sql, values)
                # self.db.commit()
      
                sql1 = "SELECT id FROM cameras WHERE rtsp = %s"
                cursor.execute(sql1, (value,))
                # Lấy kết quả trả về (ID)
                ID_rtsp = cursor.fetchone()
                sql2 = "SELECT id FROM listsvehicle WHERE name = %s"
                selected_item = self.comboBox_list_link.currentText()
                cursor.execute(sql2, (selected_item,))
                # Lấy kết quả trả về (ID)
                ID_list = cursor.fetchone()
                if ID_list and ID_rtsp:
                    list_vehicle_id = ID_list[0]
                    camera_id = ID_rtsp[0]

                    sql_insert_camera_detail = "INSERT INTO cameradetail (camera_id, list_vehicle_id) VALUES (%s, %s)"
                    id_detail = (camera_id, list_vehicle_id,)
                    cursor.execute(sql_insert_camera_detail,id_detail)
                    # Lưu thay đổi vào cơ sở dữ liệu
                    db.commit()


    def button_xoa_vitri(self):
        db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        cursor = db.cursor()
        selected_item = self.comboBox_list_link.currentText()
        index = self.comboBox_list_link.findText(selected_item)
        if index != -1:
            self.comboBox_list_link.removeItem(index)

        update_query = "UPDATE listsvehicle SET status = 0 WHERE name = %s"
        cursor.execute(update_query, (selected_item,))
        db.commit()
        ID_list = None
        sql5 = "SELECT id FROM listsvehicle WHERE name = %s"
        cursor.execute(sql5, (selected_item,))
        ID_list = cursor.fetchone()
        if ID_list is not None:
            ID_list = ID_list[0]
            sql6 = "DELETE FROM listvehicledetail WHERE list_vehicle_id = %s"
            values = (ID_list,)
            cursor.execute(sql6, values)
            db.commit()
            sql6 = "DELETE FROM cameradetail WHERE list_vehicle_id = %s"
            values = (ID_list,)
            cursor.execute(sql6, values)
            db.commit()

        # ID_list = None
        # sql2 = "SELECT id FROM listsvehicle WHERE name = %s"
        # cursor.execute(sql2, (selected_item,))
        # # Lấy kết quả trả về (ID)
        # ID_list = cursor.fetchone()
        # if ID_list is not None:
        #     ID_list = ID_list[0]

        #     sql = "DELETE FROM cameradetail WHERE list_vehicle_id = %s"
        #     values = (ID_list,)
        #     cursor.execute(sql, values)
        #     self.db.commit()

        #     id_vehicles = None
        #     sql7 = "SELECT vehicle_id FROM listvehicledetail WHERE list_vehicle_id = %s"
        #     values = (ID_list,)
        #     cursor.execute(sql7, values)
        #     id_vehicles = cursor.fetchall()
        #     for id_vehicle in id_vehicles:
        #         sql8 = "DELETE FROM vehicles WHERE id = %s"
        #         values = (id_vehicle,)
        #         cursor.execute(sql8, values)
        #         self.db.commit()

        #     sql3 = "DELETE FROM listvehicledetail WHERE list_vehicle_id = %s"
        #     values = (ID_list,)
        #     cursor.execute(sql3, values)
        #     self.db.commit()

        #     sql4 = "DELETE FROM records WHERE list_vehicle_id = %s"
        #     values = (ID_list,)
        #     cursor.execute(sql4, values)
        #     self.db.commit()
        #     ID_camera = None
        #     sql5 = "SELECT camera_id FROM cameradetail WHERE list_vehicle_id = %s"
        #     cursor.execute(sql5, (ID_list,))
        #     ID_camera = cursor.fetchone()
        #     if ID_camera is not None:
        #         ID_camera = ID_camera[0]

        #         sql6 = "DELETE FROM cameras WHERE id = %s"
        #         values = (ID_camera,)
        #         cursor.execute(sql6, values)
        #         self.db.commit()

        #     sql1 = "DELETE FROM listsvehicle WHERE name = %s"
        #     values = (selected_item,)
        #     cursor.execute(sql1, values)
        #     self.db.commit()


    def button_xoa_RTSP(self):
        db = mysql.connector.connect(user='vehicle-identification', password='aipt2023',
                             host='192.168.1.89', database='vehicle-identification')
        cursor = db.cursor(buffered=True)
        selected_item = self.comboBox_child.currentText()
        index = self.comboBox_child.findText(selected_item)
        if index != -1:
            self.comboBox_child.removeItem(index)

        sql2 = "SELECT id FROM cameras WHERE rtsp = %s"
        cursor.execute(sql2, (selected_item,))
        # Lấy kết quả trả về (ID)
        ID_rtsp = cursor.fetchone()
        ID_rtsp = ID_rtsp[0]
        cursor = db.cursor(buffered=True)
        sql = "DELETE FROM cameradetail WHERE camera_id = %s"
        values = (ID_rtsp,)
        cursor.execute(sql, values)
        db.commit()
        cursor = db.cursor(buffered=True)

        update_query = "UPDATE cameras SET status = 0 WHERE rtsp = %s"
        cursor.execute(update_query, (selected_item,))
        db.commit()
        # sql = "DELETE FROM cameras WHERE rtsp = %s"
        # values = (selected_item,)
        # cursor.execute(sql, values)
        # self.db.commit()


    def openFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Mở Tệp", "", "Tất cả các Tệp (*);;Tệp Văn Bản (*.txt);;Tệp Hình Ảnh (*.jpg *.png)", options=options)

        if file_path:
            # Xử lý tệp tin ở đây, ví dụ: in đường dẫn ra console
            print("Đường dẫn tệp đã chọn:", file_path)
            self.text_edit_RTSP.setText(file_path)    

    def closeEvent(self, event):
        # Lưu dữ liệu khi thoát chương trình
        self.save_data_to_mysql(0)
        self.db.close()    
def main():
    global ui
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
if __name__ == "__main__":
    main()
    sys.exit(app.exec_())