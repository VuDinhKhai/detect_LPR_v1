import time
from PyQt5.QtWidgets import  QFileDialog
import cv2
import pytz
from config import DB_USER,DB_PASS,DB_HOST,DB_NAME,image_directory
import mysql.connector
import main as main_Window
import main_image as main_image
import pytz
import os
import uuid
from datetime import datetime, timedelta
value_feature = 1
db = mysql.connector.connect(user=DB_USER, password=DB_PASS,
                              host=DB_HOST, database=DB_NAME)
cursor = db.cursor(buffered=True)


def get_full_id_From_listsvehicle_WHERE_name(name):
     cursor = db.cursor(buffered=True)
     sql2 = "SELECT id FROM listsvehicle WHERE name = %s"
     cursor.execute(sql2, (name,))
     results = cursor.fetchall()
     return results if results else None

def get_full_name_From_listsvehicle_status_True():
     cursor = db.cursor(buffered=True)
     cursor.execute("SELECT name FROM listsvehicle WHERE status = 1")
     results = cursor.fetchall()
     return results if results else None

def get_full_rtsp_From_name_listvehicle(name):
     cursor = db.cursor(buffered=True)
     ID_list_ = get_full_id_From_listsvehicle_WHERE_name(name)
     for ID_list in ID_list_:
          ID_list = ID_list[0]
          ID_camera_ = None
          cursor = db.cursor(buffered=True)
          sql5 = "SELECT camera_id FROM cameradetail WHERE list_vehicle_id = %s"
          cursor.execute(sql5, (ID_list,))
          ID_camera_ = cursor.fetchall()
          list_results = []
          if ID_camera_ is not None:
               for ID_camera in ID_camera_:
                    ID_camera = ID_camera[0]
                    sql3 = "SELECT rtsp FROM cameras WHERE id = %s"
                    cursor.execute(sql3, (ID_camera,))
                    results = cursor.fetchall()
                    if results is not None:
                         result = "%s" % results[0]
                         list_results.append(str(result))
          else:
               return None
          return list_results if list_results else ""

def add_LP_to_report(frame,value_LP,name_list_vehicle,rtsp,value_feature):
     cursor = db.cursor(buffered=True)
     cursor.execute("SELECT id FROM listsvehicle WHERE name = %s", (name_list_vehicle,))
     id_list_ = cursor.fetchone()
     id_list_vehicle = id_list_[0]
     
     cursor.execute("SELECT id FROM vehicles WHERE license_plate = %s", (value_LP,))
     id_LP = cursor.fetchone()
     if id_LP is not None and id_list_vehicle is not None:
          id_LP = id_LP[0]
          query = "SELECT * FROM listvehicledetail WHERE list_vehicle_id = %s AND vehicle_id = %s"
          cursor.execute(query, (id_list_vehicle,id_LP))
          print("id_list_vehicle = %s" % id_list_vehicle + " and vehicle_id = %s" % (id_LP))
          existing_camera = cursor.fetchone()
          if existing_camera is not None:
               vehicle_id = None
               time_from_database = datetime.now()
               query = "SELECT vehicle_id, time FROM records ORDER BY time DESC LIMIT 1"
               cursor.execute(query)
               row = cursor.fetchone()
               if row:
                    vehicle_id, time_from_database = row

               id_rtsp = None
               cursor.execute("SELECT id FROM cameras WHERE rtsp = %s", (rtsp,))
               id_rt = cursor.fetchone()
               id_rtsp = id_rt[0]


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
               
               if id_LP != vehicle_id:
                    cv2.imwrite(path, frame)
                    # sql = "INSERT INTO records (camera_id,list_vehicle_id,vehicle_id,feature_id,time,path) VALUES (%s,%s,%s,%s,%s,%s)"
                    insert_query = """
                    INSERT INTO records (camera_id, list_vehicle_id, vehicle_id, time, path)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    values = (id_rtsp, id_list_vehicle, id_LP, formatted_time, path)
                    # values = (id_rtsp,id_list_vehicle,id_LP,id_feature,formatted_time,path)
                    cursor.execute(insert_query, values)
                    db.commit()

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
                    db.commit()

               else:
                    current_time = datetime.now()
                    time_difference = current_time - time_from_database
                    if time_difference > timedelta(seconds=60):   
                         cv2.imwrite(path, frame)
                         insert_query = """
                         INSERT INTO records (camera_id, list_vehicle_id, vehicle_id, time, path)
                         VALUES (%s, %s, %s, %s, %s)
                         """
                         values = (id_rtsp, id_list_vehicle, id_LP, formatted_time, path,)
                         cursor.execute(insert_query, values)
                         db.commit()
                         record_id = None
                         cursor.execute("SELECT id FROM records WHERE camera_id = %s AND list_vehicle_id = %s AND vehicle_id = %s AND path = %s", (id_rtsp, id_list_vehicle, id_LP, path))
                         record_id_ = cursor.fetchone()
                         record_id = record_id_[0]
                         
                         insert_query_reportdetail = """
                         INSERT INTO recorddetail (feature_id,record_id)
                         VALUES (%s, %s)
                         """
                         values = (id_feature, record_id)
                         cursor.execute(insert_query_reportdetail, values)
                         db.commit()
          else:
               print("Biển số không ở cổng này")
def add_list_vehicle(list):
     cursor = db.cursor(buffered=True)
     status = 1
     query = "SELECT * FROM listsvehicle WHERE name = %s"
     cursor.execute(query, (list,))
     existing_camera = cursor.fetchone()
     if existing_camera is None:
          insert_query = "INSERT INTO listsvehicle (name, status) VALUES (%s, %s)"
          cursor.execute(insert_query, (list,status ))
          db.commit()
     else:
          update_query = "UPDATE listsvehicle SET status = 1 WHERE name = %s"
          cursor.execute(update_query, (list,))
          db.commit()

def add_rtsp(list,rtsp):
     cursor = db.cursor(buffered=True)
     status = 1
     query = "SELECT * FROM cameras WHERE rtsp = %s"
     cursor.execute(query, (rtsp,))
     existing_camera = cursor.fetchone()

     if existing_camera is None:
          insert_query = "INSERT INTO cameras (name,rtsp, status) VALUES (%s, %s,%s)"
          cursor.execute(insert_query, (list,rtsp, status))
          db.commit()
     else:
          update_query = "UPDATE cameras SET status = 1 WHERE rtsp = %s"
          cursor.execute(update_query, (rtsp,))
          db.commit()

def add_camerasdetail(list,rtsp):
     cursor = db.cursor(buffered=True)
     sql1 = "SELECT id FROM cameras WHERE rtsp = %s"
     cursor.execute(sql1, (rtsp,))
     ID_rtsp = cursor.fetchone()
     
     sql2 = "SELECT id FROM listsvehicle WHERE name = %s"
     cursor.execute(sql2, (list,))
     ID_list = cursor.fetchone()

     if ID_list and ID_rtsp:
          list_vehicle_id = ID_list[0]
          camera_id = ID_rtsp[0]

          sql_insert_camera_detail = "INSERT INTO cameradetail (camera_id, list_vehicle_id) VALUES (%s, %s)"
          id_detail = (camera_id, list_vehicle_id,)
          cursor.execute(sql_insert_camera_detail,id_detail)
          db.commit()

def remove_list(name_list):
     cursor = db.cursor(buffered=True)
     update_query = "UPDATE listsvehicle SET status = 0 WHERE name = %s"
     cursor.execute(update_query, (name_list,))
     db.commit()
     ID_list = None
     sql5 = "SELECT id FROM listsvehicle WHERE name = %s"
     cursor.execute(sql5, (name_list,))
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

def remove_rtsp(rtsp):
     cursor = db.cursor(buffered=True)
     sql2 = "SELECT id FROM cameras WHERE rtsp = %s"
     cursor.execute(sql2, (rtsp,))
     ID_rtsp = cursor.fetchone()
     ID_rtsp = ID_rtsp[0]

     sql = "DELETE FROM cameradetail WHERE camera_id = %s"
     values = (ID_rtsp,)
     cursor.execute(sql, values)
     db.commit()

     update_query = "UPDATE cameras SET status = 0 WHERE rtsp = %s"
     cursor.execute(update_query, (rtsp,))
     db.commit()

def openFile():
     options = QFileDialog.Options()
     file_path, _ = QFileDialog.getOpenFileName(None, "Mở Tệp", "", "Tất cả các Tệp (*);;Tệp Văn Bản (*.txt);;Tệp Hình Ảnh (*.jpg *.png)", options=options)

     if file_path:
          return file_path

def remove_LP(LP):
     cursor = db.cursor(buffered=True)
     ID_vehicle_ = None
     sql2 = "SELECT id FROM vehicles WHERE license_plate = %s"
     cursor.execute(sql2, (LP,))
     ID_vehicle_ = cursor.fetchall()
     for ID_vehicle in ID_vehicle_:
          ID_vehicle = ID_vehicle[0]
          sql4 = "DELETE FROM listvehicledetail WHERE  vehicle_id = %s"
          values = (ID_vehicle,)
          cursor.execute(sql4, values)
          db.commit()

          update_query = "UPDATE vehicles SET status = 0 WHERE id = %s"
          cursor.execute(update_query, (ID_vehicle,))
          db.commit()

def get_full_LP_from_vehicle_status_true():
     cursor = db.cursor(buffered=True)
     cursor.execute("SELECT license_plate FROM vehicles WHERE status = 1")
     results = cursor.fetchall()
     return results if results else None

def add_LP(LP):
     cursor = db.cursor(buffered=True)
     status = 1
     query = "SELECT * FROM vehicles WHERE license_plate = %s"
     cursor.execute(query, (LP,))
     existing_camera = cursor.fetchone()
     if existing_camera is None:
          insert_query = "INSERT INTO vehicles (license_plate,vehicle_campany_id,status) VALUES (%s,%s,%s)"
          cursor.execute(insert_query, (LP,main_Window.vehicle_company_id,status,))
          db.commit()
     else:
          update_query = "UPDATE vehicles SET status = 1 WHERE license_plate = %s"
          cursor.execute(update_query, (LP,))
          db.commit()

def add_vehicledetail(LP,list):
     cursor = db.cursor(buffered=True)
     sql2 = "SELECT id FROM vehicles WHERE license_plate = %s"
     cursor.execute(sql2, (LP,))
     ID_bienso = cursor.fetchone()

     sql3 = "SELECT id FROM listsvehicle WHERE name = %s"
     cursor.execute(sql3, (list,))
     ID_list = cursor.fetchone()

     if ID_list and ID_bienso:
          list_vehicle_id = ID_list[0]
          bienso_id = ID_bienso[0]

          sql_insert_bienso_detail = "INSERT INTO listvehicledetail (list_vehicle_id, vehicle_id) VALUES (%s, %s)"
          id_detail = (list_vehicle_id,bienso_id,)
          cursor.execute(sql_insert_bienso_detail,id_detail)
          db.commit()

def fetch_data():
     cursor = db.cursor(buffered=True)
     query = "SELECT * FROM records"
     cursor.execute(query)
     data = cursor.fetchall()
     return data

def fetch_data_with_rtsp_and_time(camera_id,start_time,end_time):
     cursor = db.cursor(buffered=True)
     query = f"SELECT * FROM records WHERE camera_id = {camera_id} AND time BETWEEN '{start_time}' AND '{end_time}'"
     cursor.execute(query)
     camera_info = cursor.fetchall()
     return camera_info


def fetch_data_with_rtsp(camera_id):
     cursor = db.cursor(buffered=True)
     query = f"SELECT * FROM records WHERE camera_id = {camera_id}"
     cursor.execute(query)
     camera_info = cursor.fetchall()
     return camera_info


def fetch_data_with_time(start_time,end_time):
     cursor = db.cursor(buffered=True)
     query = f"SELECT * FROM records WHERE time BETWEEN '{start_time}' AND '{end_time}'"
     cursor.execute(query)
     camera_info = cursor.fetchall()
     return camera_info

def fetch_data_with_id_LP(id_LP):
     cursor = db.cursor(buffered=True)
     query = f"SELECT * FROM records WHERE vehicle_id = {id_LP}"
     cursor.execute(query)
     camera_info = cursor.fetchall()
     return camera_info


def fetch_data_with_id_LP_and_time(id_LP,start_time,end_time):
     cursor = db.cursor(buffered=True)
     query = f"SELECT * FROM records WHERE vehicle_id = {id_LP} AND time BETWEEN '{start_time}' AND '{end_time}'"
     cursor.execute(query)
     camera_info = cursor.fetchall()
     return camera_info

def fetch_data_with_id_LP_and_list_vehicle(id_LP,rtsp_id):
     cursor = db.cursor(buffered=True)
     query = "SELECT * FROM records WHERE camera_id = %s AND vehicle_id = %s "
     cursor.execute(query, (rtsp_id,id_LP,))
     camera_info = cursor.fetchall()
     return camera_info

def fetch_data_with_id_LP_and_list_vehicle_and_time(id_LP,rtsp_id,start_time,end_time):
     query = "SELECT * FROM records WHERE camera_id = %s AND vehicle_id = %s AND time BETWEEN %s AND %s"
     cursor.execute(query, (rtsp_id,id_LP,start_time,end_time,))
     camera_info = cursor.fetchall()
     return camera_info

def fetch_camera_info(camera_id):
     cursor = db.cursor(buffered=True)
     query = f"SELECT rtsp FROM cameras WHERE id = {camera_id}"
     cursor.execute(query)
     camera_info = cursor.fetchone()
     return camera_info[0] if camera_info else ""

def fetch_list_vehicle_info(list_vehicle_id):
     cursor = db.cursor(buffered=True)
     query = f"SELECT name FROM listsvehicle WHERE id = {list_vehicle_id}"
     cursor.execute(query)
     list_vehicle_info = cursor.fetchone()
     return list_vehicle_info[0] if list_vehicle_info else ""

def fetch_vehicle_info(vehicle_id):
     cursor = db.cursor(buffered=True)
     query = f"SELECT license_plate FROM vehicles WHERE id = {vehicle_id}"
     cursor.execute(query)
     vehicle_info = cursor.fetchone()
     return vehicle_info[0] if vehicle_info else ""

def fetch_feature_info(feature_id):
     cursor = db.cursor(buffered=True)
     query = f"SELECT name FROM features WHERE id = {feature_id}"
     cursor.execute(query)
     feature_info = cursor.fetchone()
     return feature_info[0] if feature_info else ""

def get_list_and_rtsp():
     cursor = db.cursor(buffered=True)
     list_results = []
     cursor.execute("SELECT id FROM listsvehicle")
     for row in cursor.fetchall():
          row = row[0]
          Name_list_ = None
          sql2 = "SELECT name FROM listsvehicle WHERE id = %s"
          cursor.execute(sql2, (row,))
          Name_list_ = cursor.fetchall()
          for name in Name_list_:
               Name_list = str(name[0])
          ID_camera = None
          sql5 = "SELECT camera_id FROM cameradetail WHERE list_vehicle_id = %s"
          cursor.execute(sql5, (row,))
          ID_camera_ = cursor.fetchall()
          for ID_camera in ID_camera_:
               ID_camera = ID_camera[0]
               cursor = db.cursor(buffered=True)
               sql3 = "SELECT rtsp FROM cameras WHERE id = %s"
               cursor.execute(sql3, (ID_camera,))
               results = cursor.fetchall()
               for result in results:
                    results = Name_list + "/" + str(result[0])
                    list_results.append(results)
     return list_results

def get_id_camera_where_rtsp(rtsp):
     cursor = db.cursor(buffered=True)
     sql2 = "SELECT id FROM cameras WHERE rtsp = %s"
     cursor.execute(sql2, (rtsp,))
     # Lấy kết quả trả về (ID)
     results = cursor.fetchall()
     return results if results else None

def get_id_vehicle_where_LP(LP):
     cursor = db.cursor(buffered=True)
     cursor.execute("SELECT id FROM vehicles WHERE license_plate = %s", (LP,))
     results = cursor.fetchall()
     return results if results else None
     
def main():
    pass

if __name__ == "__main__":
     main()
     


