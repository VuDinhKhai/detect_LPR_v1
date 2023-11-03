from PyQt5 import  QtWidgets
import Setup_main as main_Window
import sys
from PyQt5.QtWidgets import  QComboBox, QMainWindow
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt
import sql as aiptsql
import sys
from Display.ADD1_display import Ui_MainWindow
import logging
app = QtWidgets.QApplication(sys.argv)

MainWindow1 = QtWidgets.QMainWindow()
ui = ''
class CheckableComboBox(QComboBox):
     def __init__(self):
          super(CheckableComboBox, self).__init__()
          self.view().pressed.connect(self.handle_item_pressed)
          self.setModel(QStandardItemModel(self))
          for i in range(self.count()):
               item = self.model().item(i)
               item.setCheckable(True)
               item.setCheckState(Qt.Checked)
               self.check_items()

     # when any item get pressed
     def handle_item_pressed(self, index):

          # getting which item is pressed
          item = self.model().itemFromIndex(index)

          # make it check if unchecked and vice-versa
          if item.checkState() == Qt.Checked:
               item.setCheckState(Qt.Unchecked)
          else:
               item.setCheckState(Qt.Checked)

          # calling method
          self.check_items()

     # method called by check_items
     def item_checked(self, index):

          # getting item at index
          item = self.model().item(index, 0)

          # return true if checked else false
          return item.checkState() == Qt.Checked

          # calling method
     def check_items(self):
          # blank list
          checkedItems = []

          # traversing the items
          for i in range(self.count()):

               # if item is checked add it to the list
               if self.item_checked(i):
                    checkedItems.append(i)

          # call this method
          self.update_labels(checkedItems)
          return checkedItems

     # method to update the label
     def update_labels(self, item_list):
          n = ''
          count = 0
          # traversing the list
          for i in item_list:
               # if count value is 0 don't add comma
               if count == 0:
                    n += ' % s' % i
               # else value is greater than 0
               # add comma
               else:
                    n += ', % s' % i

               # increment count
               count += 1


          # loop
          for i in range(self.count()):

               # getting label
               text_label = self.model().item(i, 0).text()
               # default state
               if text_label.find('-') >= 0:
                    text_label = text_label.split('-')[0]

               # shows the selected items
               item_new_text_label = text_label + ' - Chọn list số : ' + n
               # item_new_text_label = text_label
               # setting text to combo box
               self.setItemText(i,text_label)
          # return item_list
     def default_setup(self):
          for i in range(self.count()):
               item = self.model().itemFromIndex(i)
               print(item)
               if item.checkState() == Qt.UnChecked:
                    item.setCheckState(Qt.checked)
    # flush
    # sys.stdout.flush()

class UiMainWindow(QMainWindow):
     global ui 
     def __init__(self):
          super().__init__()
          self.ui = Ui_MainWindow()  # Tạo đối tượng giao diện
          self.ui.setupUi(self)  # Thiết lập giao diện cho cửa sổ chính
          self.showMaximized()
          self.ui.retranslateUi(self) 

          self.ui.Button_quaylai.clicked.connect(self.button_thoat)
          self.ui.comboBox_listxe.currentIndexChanged.connect(self.select_combobox_listxe)
          self.ui.Button_xoalistxe.clicked.connect(self.button_xoalistxe)
          self.ui.Button_xoabienso.clicked.connect(self.button_xoa_bienso)
          self.load_data_to_combobox_listxe()
          self.ui.comboBox_list_bienso.currentIndexChanged.connect(self.select_combobox_listbienso)
          self.ui.Button_luu.clicked.connect(self.them_bienso)
     
     
     
     def button_thoat(self):
          global ui
          ui.hide()
          # ui = main_Window._main_()
     def select_combobox_listxe(self):
          self.ui.label_hiendanhsach.clear()
          self.ui.comboBox_list_bienso.clear()
          index = self.ui.comboBox_listxe.check_items()
          hiendanhsach = "" 
          for i in index:
               text_label = self.ui.comboBox_listxe.model().item(i, 0).text()
               hiendanhsach = hiendanhsach + text_label +  "-"
          selected_vehicle_ids = aiptsql.get_id_vehicle_where_list_vehicle(hiendanhsach)
          if selected_vehicle_ids is not None:
               for result in selected_vehicle_ids:
                    self.ui.comboBox_list_bienso.addItem(result)
          self.ui.label_hiendanhsach.setText(f"{hiendanhsach}")



     def button_xoalistxe(self):
          index = self.ui.comboBox_listxe.check_items()
          cont = 0
          print("index = " + str(index))
          if len(index) > 0:
               for i in index:
                    item_text = self.ui.comboBox_listxe.itemText(i-cont)
                    self.ui.comboBox_listxe.removeItem(i - cont)
                    print("item_text = ", item_text)
                    aiptsql.remove_list(item_text)
                    
                    cont = cont + 1
     def button_xoa_bienso(self):
          selected_item = self.ui.comboBox_list_bienso.currentText()
          index = self.ui.comboBox_list_bienso.findText(selected_item)
          if index != -1:
               self.ui.comboBox_list_bienso.removeItem(index)
          self.ui.label_hiendanhsach.setText("         Đã xóa biển số  : " + selected_item)
          
          aiptsql.remove_LP(selected_item)

     def load_data_to_combobox_listxe(self):
          results = aiptsql.get_full_name_From_listsvehicle_status_True()
          if results is not None:
               for result in results:
                    self.ui.comboBox_listxe.addItem(result[0])
          
          # results = aiptsql.get_full_LP_from_vehicle_status_true()
          # if results is not None:
          #      for result in results:
          #           self.ui.comboBox_list_bienso.addItem(result[0])

     def select_combobox_listbienso(self):
          selected_item = self.ui.comboBox_list_bienso.currentText()
          # self.ui.label_hienbienso.setText(f"{selected_item}")


     def them_bienso(self):
          value = self.ui.Edit_bienso.toPlainText()
          index1 = self.ui.comboBox_listxe.check_items()
          if len(value) !=0:
               found = True
               for index in range(self.ui.comboBox_list_bienso.count()):
                    item_text = self.ui.comboBox_list_bienso.itemText(index)
                    if item_text == value:
                         found = False
                         break
               print("index : " + str(index1))
               if found and len(index1) > 0:
                    self.ui.comboBox_list_bienso.addItem(value)
                    self.ui.label_hienbienso.setText("         Đã thêm biển số : " + value)
                    aiptsql.add_LP(value)
                    # index3 = self.comboBox_listxe.check_items()
                    for i in index1:
                         text_label = self.ui.comboBox_listxe.model().item(i, 0).text()

                         aiptsql.add_vehicledetail(value, text_label) 



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