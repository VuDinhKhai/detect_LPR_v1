# import main_image as main_image
import sql as aiptsql
import form_list as formlist
import report as report_window
import add as ADD
import form_reco as form_reco
import time
import cv2
import numpy as np
from PyQt5.QtCore import Qt,pyqtSignal,QThread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from config import image_directory,file_log
import sys
from PyQt5.QtWidgets import QMainWindow
from Display.main_v1 import Ui_MainWindow
import inspect
import logging
import concurrent.futures
import LPR.plateAnalyze_2 as plateAnalyze_2
detect= False
plateAnalyze = plateAnalyze_2.Detection()

app = QtWidgets.QApplication(sys.argv)
# MainWindow1 = QtWidgets.QMainWindow()
ui =''
thread = {}
vehicle_company_id = 1
import os
from datetime import datetime, timedelta
import os
from datetime import datetime, timedelta


class UiMainWindow(QMainWindow):
     global thread , ui 
     def __init__(self):
          super().__init__()
          
          self.ui = Ui_MainWindow()  # Tạo đối tượng giao diện
          # self.ui.showMaximized()
          self.ui.setupUi(self)  # Thiết lập giao diện cho cửa sổ chính
          self.showMaximized()
          self.ui.retranslateUi(self) 
          self.ui.Buttonfile.clicked.connect(self.button_formlist)
          self.ui.Buttoncam.clicked.connect(self.button_camera)
          self.ui.Button_setting.clicked.connect(self.button_setting)  
          self.ui.Button_Reco.clicked.connect(self.button_LPR)       
          self.ui.Button_baocao.clicked.connect(self.button_bc)
          self.ui.combobox_list.currentIndexChanged.connect(self.select_combobox)
          

          self.ui.combobox_list.currentIndexChanged.connect(self.select_combobox)
          
          self.ui.comboBox.currentIndexChanged.connect(self.select_combobox_RTSP)

          self.load_data_to_combobox_list_and_rtsp()

          try:
               if aiptsql.get_1_status_camera_view():
                    self.start_capture_video()
          except Exception as e:
              logging.error("243 error :  %s", str(e))

          # Đặt đường dẫn đến thư mục chứa các tệp nhật ký
          log_directory = file_log

          # Xác định ngày hôm trước
          yesterday = datetime.now() - timedelta(days=1)

          # Định dạng ngày thành chuỗi theo định dạng yyyy-mm-dd
          yesterday_str = yesterday.strftime("%Y-%m-%d")

          # Lặp qua các tệp trong thư mục và kiểm tra xem tệp có ngày trùng với ngày hôm trước không
          for filename in os.listdir(log_directory):
               if yesterday_str in filename:
                    file_path = os.path.join(log_directory, filename)
                    os.remove(file_path)
                    print(f"Đã xóa tệp: {filename}")

     def button_formlist(self):
          try:
               global ui
               ui = formlist.main()  
          except Exception as e:
              logging.error("button_formlist %s", str(e))
     def show_webcam1(self, frame):
          qt_frame = self.convert_cv_qt(frame)
          self.ui.viewcam1.setPixmap(qt_frame)
     def button_LPR(self):
          global detect 
          detect = not detect

     def button_setting(self):
          try:
               print("nhan button setting")
               global ui
               ui = ADD.main()
          except Exception as e:
              logging.error("button_setting %s", str(e))  
          
     def button_bc(self):
          try:
               print("nhan button baocao")
               global ui
               ui = report_window.main()
          except Exception as e:
              logging.error("button_baocao %s", str(e))  


     def convert_cv_qt(self, cv_img):
          """Convert from an opencv image to QPixmap"""
          rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
          h, w, ch = rgb_image.shape
          bytes_per_line = ch * w
          convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
          p = convert_to_Qt_format.scaled(1280 , 720, Qt.KeepAspectRatio)
          return QPixmap.fromImage(p) 
     def button_camera(self):
          print("nhan button camera")
          rtsp = self.select_combobox_RTSP()
          list_name = self.comboBox_list_current()
          self.stop_capture_video()
          name_rtsp_and_list = aiptsql.get_1_status_camera_view()
          if name_rtsp_and_list:
               name_list_pre, rtsp_pre = name_rtsp_and_list[0]
               if name_list_pre is not None and rtsp_pre is not None:
                    if rtsp != rtsp_pre or list_name != name_list_pre:
                         aiptsql.set_status_camera_view(rtsp,list_name)
                         self.start_capture_video()
          else:
               aiptsql.set_status_camera_view(rtsp,list_name)
               self.start_capture_video()

     def start_capture_video(self):
          thread[1] = capture_video(index=1)
          thread[1].start()
          thread[1].signal.connect(self.show_webcam1)
  
     def log_current_line():
          current_frame = inspect.currentframe()
          line_number = current_frame.f_back.f_lineno  # Lấy số dòng hiện tại
          logging.debug(f'Current line: {line_number}')

     def load_data_to_combobox_list_and_rtsp(self):
          results = aiptsql.get_full_name_From_listsvehicle_status_True()
          if results is not None:
               for result in results:
                    result = result[0]
                    self.ui.combobox_list.addItem(result)

     def select_combobox(self):
          selected_item = self.ui.combobox_list.currentText()
          self.ui.comboBox.clear()
          results = aiptsql.get_full_rtsp_From_name_listvehicle(selected_item)
          if len(results):
               for result in results:
                    self.ui.comboBox.addItem(result)
     def select_combobox_RTSP(self):
          selected_item = self.ui.comboBox.currentText()
          return selected_item
     def comboBox_list_current(self):
          selected_item = self.ui.combobox_list.currentText()
          return selected_item   
     def stop_capture_video(self):
          # self.thread[1].signal.disconnect(self.show_webcam)
          thread[1].stop()
value_LP1 = None
value_feature = 1
import logging
from datetime import datetime

class capture_video(QThread):
     global detect,ui,value_LP1,value_feature,image_directory
     signal = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,


     def __init__(self,index):
          self.index = index         # index = 1 -> capture_video là luồng 1
          print("Start threading : ", self.index)
          super(capture_video, self).__init__()   # thừa hưởng , tái khẳng định
          self.stopped = False 
          self.start_time = datetime.now()

     def process_frame(self,frame,name_list_vehicle, rtsp, value_feature):
          value_LP1 = None
          frame, value_LP1 = frame,value_LP1 = plateAnalyze.detect(frame)
          
          if value_LP1 is not None:
               print("Value : " + str(value_LP1))
               for value in value_LP1:
                    aiptsql.add_LP_to_report(frame, value, name_list_vehicle, rtsp, value_feature)
          return frame
     def run(self):
          # Lấy thông tin camera và danh sách xe
          name_rtsp_and_list = aiptsql.get_1_status_camera_view()
          if name_rtsp_and_list:
               name_list_vehicle, rtsp = name_rtsp_and_list[0]
          else:
               rtsp = name_list_vehicle = 0
          print("rtsp: " + str(rtsp) + "  name_list_vehicle: " + str(name_list_vehicle))
          if rtsp == "0":
               rtsp = 0
          cap = cv2.VideoCapture(rtsp)
          frame_count = 0
          delay_frames = 4
          
          with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
               while not self.stopped:
                    ret, frame = cap.read()
                    frame_count += 1

                    # Tính thời gian trôi qua từ lúc bắt đầu
                    elapsed_time = (datetime.now() - self.start_time).total_seconds()

                    if frame_count % delay_frames == 0:
                         if ret:
                              if detect:
                                   try:
                                        future = executor.submit(self.process_frame, frame,name_list_vehicle, rtsp, value_feature)
                                        frame = future.result()
                                   except Exception as e:
                                        logging.error("detect : Loi khi phat hien doi tuong: %s", str(e))   

                               # Tính FPS
                              fps = frame_count / elapsed_time

                              # Hiển thị FPS lên khung hình
                              cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                              self.signal.emit(frame)  # Gửi frame sau khi xử lý
                         else:
                              break

     def stop(self):
          print("Stop threading : ", self.index)
          self.stopped = True 
          self.terminate()
          
class capture_video1(QThread):
     global detect,ui,value_LP1,value_feature,image_directory,plateAnalyze
     signal = pyqtSignal(np.ndarray)   # signal suất đi kiểu np.ndarray , nếu suất đi số là int , chữ là string ,


     def __init__(self,index):
          self.index = index         # index = 1 -> capture_video là luồng 1
          print("Start threading : ", self.index)
          super(capture_video1, self).__init__()   # thừa hưởng , tái khẳng định
          self.stopped = False 
     def run(self):
          # rtsp = self.ui_main_window.select_combobox_RTSP()
          name_rtsp_and_list = aiptsql.get_1_status_camera_view()
          if name_rtsp_and_list:
               name_list_vehicle, rtsp = name_rtsp_and_list[0]
          else:
               rtsp = name_list_vehicle = 0
          print("rtsp: "+ str(rtsp) + "  name_list_vehicle: "+str( name_list_vehicle))
          if rtsp == "0":
               rtsp = 0 
          cap = cv2.VideoCapture(rtsp)
          frame_count = 0
          delay_frames = 12
          while not self.stopped:
               ret, frame = cap.read()
               if ret:
                    if detect:
                         if frame_count % delay_frames == 0:
                              try:
                                   # frame,value_LP1 = main_image.detect_APP1(weights_detect,weights_reco,frame)
                                   frame,value_LP1 = plateAnalyze.detect(frame)
                                   if value_LP1 != None:
                                        aiptsql.add_LP_to_report(frame, value_LP1 ,name_list_vehicle,rtsp,value_feature)
                              except Exception as e:
                                   logging.error("detect : Loi khi phat hien doi tuong: %s", str(e))  
                              self.signal.emit(frame)
                    else:
                         self.signal.emit(frame)
               else:
                    break
          cap.release()
     def stop(self):
          print("Stop threading : ", self.index)
          self.stopped = True 
          self.terminate()     





def _main_():
     global ui
     ui = UiMainWindow()
     ui.show()

    

if __name__ == "__main__":
     try:
          # Thực hiện một thao tác nào đó
          _main_()
     except Exception as e:
          # Ghi lại lỗi nếu có
          logging.error("__name__ == __main__ : Loi chuong trinh: %s", str(e))
     sys.exit(app.exec_())