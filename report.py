from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import Setup_main as main_Window
import sys
from PyQt5.QtWidgets import  QFileDialog
import sql as aiptsql
from Display.report1_display import Ui_MainWindow
import logging
import os
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel,QDateTime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Setup_main as main_Window
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import os
import sql as aiptsql
app = QtWidgets.QApplication(sys.argv)

MainWindow1 = QtWidgets.QMainWindow()
ui = ''
current_directory = os.getcwd()
class UiMainWindow(QMainWindow):
     global ui 
     def __init__(self):
          super().__init__()
          self.ui = Ui_MainWindow()  # Tạo đối tượng giao diện
          self.ui.setupUi(self)  # Thiết lập giao diện cho cửa sổ chính
          self.showMaximized()
          self.ui.retranslateUi(self) 
          self.ui.Button_mainw.clicked.connect(self.button_mainw)
          self.load_data()
          self.ui.comboBox_nhan_videocamera.currentIndexChanged.connect(self.select_combobox)
          self.ui.Button_timkiem.clicked.connect(self.timkiem)
          self.ui.Tableview.horizontalHeader().sectionClicked.connect(self.handle_column_header_clicked)
          self.ui.Tableview.verticalHeader().sectionClicked.connect(self.handle_row_header_clicked)
          self.ui.Tableview.cellClicked.connect(self.handle_cell_clicked)
          self.ui.Button_xoa.clicked.connect(self.delete_selected_row)

          self.ui.Tableview.resizeColumnsToContents()
          self.ui.Tableview.resizeRowsToContents()
          # Thiết lập kích thước mặc định cho hàng và cột
          for row in range(self.ui.Tableview.rowCount()):
               self.ui.Tableview.setRowHeight(row, 200)  # Đặt chiều cao hàng là 200
          for col in range(self.ui.Tableview.columnCount()):
               self.ui.Tableview.setColumnWidth(col, 240)  # Đặt chiều rộng cột là 240




     def show_tableview(self,row_index,row):
          id,camera_id, list_vehicle_id, vehicle_id, time, path = row
          license_plate = aiptsql.fetch_vehicle_info(vehicle_id)
          self.ui.Tableview.setItem(row_index, 0, QTableWidgetItem(str(license_plate)))

          self.ui.Tableview.setItem(row_index, 1, QTableWidgetItem(str(time)))

          list_vehicle_ = aiptsql.fetch_list_vehicle_info(list_vehicle_id)
          self.ui.Tableview.setItem(row_index, 2 , QTableWidgetItem(str(list_vehicle_)))

          rtsp = aiptsql.fetch_camera_info(camera_id)
          self.ui.Tableview.setItem(row_index, 3 , QTableWidgetItem(str(rtsp)))

          self.ui.Tableview.setItem(row_index, 4, QTableWidgetItem(path))
          path = current_directory + "\\" + str(path)
          print("path : " + path)

          pixmap1 = QPixmap(path)
          pixmap1 = pixmap1.scaledToWidth(240)
          pixmap1 = pixmap1.scaledToHeight(200)
          item1 = QTableWidgetItem()
          item1.setData(Qt.DecorationRole, pixmap1)
          self.ui.Tableview.setItem(row_index, 5, item1)

     def button_mainw(self):
          global ui
          ui.hide()
          # ui = main_Window._main_()
     def load_data(self):
          global current_directory
          results = aiptsql.get_list_and_rtsp()
          for result in results:
               self.ui.comboBox_nhan_videocamera.addItem(result)
          data = aiptsql.fetch_data()
          if data:
               self.ui.Tableview.setRowCount(len(data))
               self.ui.Tableview.setColumnCount(len(data[0]))
               for row_index, row in enumerate(data):
                    self.show_tableview(row_index,row)
     def default_setup(self):
          self.ui.Tableview.resizeColumnsToContents()
          self.ui.Tableview.resizeRowsToContents()
          for row in range(self.ui.Tableview.rowCount()):
               self.ui.Tableview.setRowHeight(row, 200)  # Đặt chiều cao hàng là 200
          for col in range(self.ui.Tableview.columnCount()):
               self.ui.Tableview.setColumnWidth(col, 240)  # Đặt chiều rộng cột là 240
     def select_combobox(self):
          selected_item = self.ui.comboBox_nhan_videocamera.currentText()
          rtsp = None
          if selected_item != "Tat ca":

               parts = selected_item.split("--")
               if len(parts) == 2:
                    name_list = parts[0]
                    rtsp = parts[1]

                    while self.ui.Tableview.rowCount() > 0:
                         self.ui.Tableview.removeRow(0)
                    camera_id_ = None
                    camera_id_ = aiptsql.get_id_camera_where_rtsp(rtsp)
                    if camera_id_ is not None:
                         row_table = 0
                         for camera_id in camera_id_:
                              data =aiptsql.fetch_data_with_rtsp(camera_id[0])
                              if data:
                                   self.ui.Tableview.setColumnCount(len(data[0]))
                              
                                   for row_index, row in enumerate(data):
                                        self.ui.Tableview.setRowCount(row_table + 1)
                                        self.default_setup()
                                        self.show_tableview(row_table, row)
                                        row_table = row_table + 1 
          else :
               data = aiptsql.fetch_data()
               self.default_setup()
               if data:
                    self.ui.Tableview.setRowCount(len(data))
                    self.ui.Tableview.setColumnCount(len(data[0]))
                    for row_index, row in enumerate(data):
                         self.default_setup()
                         self.show_tableview(row_index, row)

     def timkiem(self):
          is_checked_bienso = self.ui.checkBox_bienso.isChecked()
          is_checked_nhanxe = self.ui.checkBox_nhanxe.isChecked()
          is_checked_mauxe = self.ui.checkBox_mauxe.isChecked()
          is_checked_soluongxe = self.ui.checkBox_soluongxe.isChecked()
          while self.ui.Tableview.rowCount() > 0:
               self.ui.Tableview.removeRow(0)
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
          date_time_start = self.ui.dateTimeEdit_start.dateTime()
          date_time_start = date_time_start.toString("yyyy-MM-dd HH:mm:ss")
          print("Selected Date and Time start:", date_time_start)
          date_time_end = self.ui.dateTimeEdit_end.dateTime()
          date_time_end = date_time_end.toString("yyyy-MM-dd HH:mm:ss")
          print("Selected Date and Time end:", date_time_end)
          selected_item = self.ui.comboBox_nhan_videocamera.currentText()
          
          seach_selected = True
          if selected_item == "Tat ca":
               seach_selected = False
          else:
               parts = selected_item.split("--")
               if len(parts) == 2:
                    name_list = parts[0]
                    rtsp_item_combobox = parts[1]

          print("Selected Item:", selected_item)
          
          text_bienso = self.ui.textEdit_bienso.toPlainText()
          
          if text_bienso and seach_selected == False:
               id_LP_ = aiptsql.get_id_vehicle_where_LP(text_bienso)
               row_table=0
               if id_LP_ :
                    for id_LP in id_LP_:
                         if date_time_end == date_time_start:
                              data = aiptsql.fetch_data_with_id_LP(id_LP[0])
                              if data:
                                   self.ui.Tableview.setColumnCount(len(data[0]))
                                   for row_index, row in enumerate(data):
                                        self.ui.Tableview.setRowCount(row_table + 1)
                                        self.default_setup()
                                        self.show_tableview(row_table, row)
                                        row_table = row_table + 1 
                         else:
                              data = aiptsql.fetch_data_with_id_LP_and_time(id_LP[0],date_time_start,date_time_end)
                              if data:
                                   self.ui.Tableview.setColumnCount(len(data[0]))
                                   for row_index, row in enumerate(data):
                                        self.ui.Tableview.setRowCount(row_table + 1)
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
                                        self.ui.Tableview.setColumnCount(len(data[0]))
                                        for row_index, row in enumerate(data):
                                             self.ui.Tableview.setRowCount(row_table + 1)
                                             self.default_setup()
                                             self.show_tableview(row_table, row)
                                             row_table = row_table + 1 
                         else:
                              data = aiptsql.fetch_data_with_id_LP_and_list_vehicle_and_time(id_LP[0],rtsp_id,date_time_start,date_time_end)
                              if data:
                                   self.ui.Tableview.setColumnCount(len(data[0]))
                                   for row_index, row in enumerate(data):
                                        self.ui.Tableview.setRowCount(row_table + 1)
                                        self.default_setup()
                                        self.show_tableview(row_table, row)
                                        row_table = row_table + 1
          elif text_bienso == "" and seach_selected == False:
               while self.ui.Tableview.rowCount() > 0:
                    self.ui.Tableview.removeRow(0)
               data =aiptsql.fetch_data_with_time(date_time_start, date_time_end)
               row_table = 0
               if data:
                    self.ui.Tableview.setColumnCount(len(data[0]))
                    for row_index, row in enumerate(data):
                         self.ui.Tableview.setRowCount(row_table + 1)
                         self.default_setup()
                         self.show_tableview(row_table, row)
                         row_table = row_table + 1    
          elif text_bienso == "" and seach_selected == True:
               parts = selected_item.split("--")
               if len(parts) == 2:
                    name_list = parts[0]
                    rtsp = parts[1]
               while self.ui.Tableview.rowCount() > 0:
                    self.ui.Tableview.removeRow(0)
               camera_id_ = None
               camera_id_ = aiptsql.get_id_camera_where_rtsp(rtsp)
               row_table = 0
               if camera_id_ is not None:
                    for camera_id in camera_id_:
                         data = aiptsql.fetch_data_with_rtsp_and_time(camera_id[0],date_time_start,date_time_end)
                         if data:
                              self.ui.Tableview.setColumnCount(len(data[0]))
                              for row_index, row in enumerate(data):
                                   self.ui.Tableview.setRowCount(row_table + 1)
                                   self.default_setup()
                                   self.show_tableview(row_table, row)
                                   row_table = row_table + 1 
          self.ui.label_tongso.setText("Tổng số " + str(self.ui.Tableview.currentRow()))
          self.table_report()

     def table_report(self):
          print("table_report")


     def handle_cell_clicked(self, row, col):
          item = self.ui.Tableview.item(row, col)
          if item:
                    print(f"Cell ({row}, {col}) clicked, value: {item.text()}")
          else:
                    print(f"Cell ({row}, {col}) clicked, no item")
          self.show_image(row)
     def handle_column_header_clicked(self, col):
          print(f'Column header clicked: {col}')

     def handle_row_header_clicked(self, row):
          print(f'Row header clicked: {row}')

     def delete_selected_row(self):
          selected_row = self.ui.Tableview.currentRow()
          if selected_row >= 0:
               self.ui.Tableview.removeRow(selected_row)

     def show_image(self , row):
          item = self.ui.Tableview.item(row,4 )
          path = item.text()
          print("path ", path)
          pixmap1 = QPixmap(path)
          pixmap1 = pixmap1.scaledToWidth(380)
          pixmap1 = pixmap1.scaledToHeight(300)

          self.ui.label_thongtintimkiem.setPixmap(pixmap1)




def main():
     global ui
     ui = UiMainWindow()
     ui.show()

    

if __name__ == "__main__":
     try:
          # Thực hiện một thao tác nào đó
          main()
     except Exception as e:
          # Ghi lại lỗi nếu có
          logging.error("__name__ == __main__ : Loi chuong trinh: %s", str(e))
     sys.exit(app.exec_())