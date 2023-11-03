from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import Setup_main as main_Window
import sys
from PyQt5.QtWidgets import  QFileDialog
import sql as aiptsql
from Display.formlist1_display import Ui_MainWindow
import logging

app = QtWidgets.QApplication(sys.argv)

MainWindow1 = QtWidgets.QMainWindow()
ui = ''
class UiMainWindow(QMainWindow):
     global ui 
     def __init__(self):
          super().__init__()
          self.ui = Ui_MainWindow()  # Tạo đối tượng giao diện
          self.ui.setupUi(self)  # Thiết lập giao diện cho cửa sổ chính
          self.showMaximized()
          self.ui.retranslateUi(self) 
          self.ui.Button_thoat.clicked.connect(self.button_thoat)
          self.ui.comboBox_list_link.currentIndexChanged.connect(self.select_combobox)
          self.ui.comboBox_child.currentIndexChanged.connect(self.select_combobox_child)
          self.ui.Button_luu_vitri.clicked.connect(self.luu_vitri)
          self.ui.Button_luu.clicked.connect(self.luu_RTSP)
          self.ui.Button_xoa_vitri.clicked.connect(self.button_xoa_vitri)
          self.ui.Button_xoa.clicked.connect(self.button_xoa_RTSP)
          self.ui.Button_mofile.clicked.connect(self.openFile)
          self.load_data_to_combobox()


          
     def load_data_to_combobox(self):
          results = aiptsql.get_full_name_From_listsvehicle_status_True()
          if results is not None:
               for row in results:
                    self.ui.comboBox_list_link.addItem(row[0])     
     
     def button_thoat(self):
          global ui
          ui.hide()
          # ui = main_Window._main_()
          
     def select_combobox(self):
          selected_item = self.ui.comboBox_list_link.currentText()
          self.ui.comboBox_child.clear()
          results = aiptsql.get_full_rtsp_From_name_listvehicle(selected_item)
          if results is not None:
               for result in results:
                    self.ui.comboBox_child.addItem(result)
          self.ui.label_cha.setText(f"{selected_item}")     
     def select_combobox_child(self):
          selected_item = self.ui.comboBox_child.currentText()
          # self.ui.text_edit_RTSP.setText(f"{selected_item}")

     def luu_vitri(self):
          value = self.ui.text_edit_RTSP.toPlainText()
          if len(value) !=0:
               found = True
               for index in range(self.ui.comboBox_list_link.count()):
                    item_text = self.ui.comboBox_list_link.itemText(index)
                    if item_text == value:
                         found = False
                         break
               if found:
                    aiptsql.add_list_vehicle(value)
                    self.ui.comboBox_list_link.addItem(value)
                    self.ui.label_cha.setText("Đã thêm : " + value)
     def luu_RTSP(self):
          value = self.ui.text_edit_RTSP.toPlainText()
          selected_item = self.ui.comboBox_list_link.currentText()
          if len(value) !=0:
               found = True
               for index in range(self.ui.comboBox_child.count()):
                    item_text = self.ui.comboBox_child.itemText(index)
                    if item_text == value:
                         found = False
                         break
               if found:            
                    self.ui.comboBox_child.addItem(value)
                    self.ui.text_edit_RTSP.setText(value)
                    aiptsql.add_rtsp(selected_item,value)
                    aiptsql.add_camerasdetail(selected_item,value)
     def button_xoa_vitri(self):
          selected_item = self.ui.comboBox_list_link.currentText()
          index = self.ui.comboBox_list_link.findText(selected_item)
          if index != -1:
               self.ui.comboBox_list_link.removeItem(index)

          aiptsql.remove_list(selected_item)

     def button_xoa_RTSP(self):
          selected_item = self.ui.comboBox_child.currentText()
          index = self.ui.comboBox_child.findText(selected_item)
          if index != -1:
               self.ui.comboBox_child.removeItem(index)

          aiptsql.remove_rtsp(selected_item)
     def openFile(self):
          file_path = aiptsql.openFile()

          # options = QFileDialog.Options()
          # file_path, _ = QFileDialog.getOpenFileName(None, "Mở Tệp", "", "Tất cả các Tệp (*);;Tệp Văn Bản (*.txt);;Tệp Hình Ảnh (*.jpg *.png)", options=options)

          # if file_path:
          #     # Xử lý tệp tin ở đây, ví dụ: in đường dẫn ra console
          print("Đường dẫn tệp đã chọn:", file_path)
          self.ui.text_edit_RTSP.setText(file_path)






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