from sqlalchemy.dialects.mssql import INTEGER, NVARCHAR, VARCHAR,DATETIME
from sqlalchemy import Column, ForeignKey
from .extension import db_base_model

class Role(db_base_model):
  __tablename__ = "Roles"
  id = Column(INTEGER, primary_key=True, autoincrement=True)
  name = Column(NVARCHAR(50), nullable=False)

  def __init__(self, name):
    self.name = name

class User(db_base_model):
  __tablename__ = "Users"
  id = Column(INTEGER, primary_key=True, autoincrement=True)
  name = Column(NVARCHAR(50), nullable=False)
  email = Column(VARCHAR(50), nullable=False, unique=True)
  phone = Column(VARCHAR(15), nullable=False, unique=True)
  password  = Column(VARCHAR(100), nullable=False)
  role_id = Column(INTEGER, ForeignKey(Role.id), nullable=False)

  def __init__(self, name, email, phone, password):
    self.name = name
    self.email = email
    self.phone = phone
    self.password = password

class ListVehicle(db_base_model):
  __tablename__ = "ListsVehicle"
  id = Column(INTEGER, primary_key=True, autoincrement=True)
  name = Column(NVARCHAR(50), nullable=False, unique=True)
  status = Column(INTEGER, nullable=False)

  def __init__(self, name, status):
    self.name = name
    self.status = status

class Camera(db_base_model):
  __tablename__ = "Cameras"
  id = Column(INTEGER, primary_key=True, autoincrement=True) 
  name = Column(NVARCHAR(100), nullable=False)
  rtsp = Column(VARCHAR(100), nullable=False, unique=True)
  status = Column(INTEGER, nullable=False)

  def __init__(self, name, rtsp, status):
    self.name = name
    self.rtsp = rtsp
    self.status = status

class CameraDetail(db_base_model):
  __tablename__ = "CameraDetail"

  id = Column(INTEGER, primary_key=True, autoincrement=True)
  camera_id = Column(INTEGER, ForeignKey(Camera.id), nullable=False)
  list_vehicle_id = Column(INTEGER, ForeignKey(ListVehicle.id), nullable=False)
  status = Column(INTEGER, nullable=False)

  def __init__(self,  camera_id, list_vehicle_id, status):
    self.camera_id = camera_id
    self.list_vehicle_id = list_vehicle_id
    self.status = status

class CamerasUser(db_base_model):
  __tablename__ = "CamerasUser"
  id = Column(INTEGER, primary_key=True, autoincrement=True) 
  camera_id = Column(INTEGER, ForeignKey(Camera.id), nullable=False)
  user_id = Column(INTEGER, ForeignKey(User.id), nullable=False)
  camera_status = Column(INTEGER, nullable=False)

  def __init__(self, camera_id, user_id, camera_status):
    self.camera_id = camera_id
    self.user_id = user_id
    self.camera_status = camera_status

class VehicleCampany(db_base_model):
  __tablename__ = "VehicleCampanys"
  id = Column(INTEGER, primary_key=True, autoincrement=True)
  name = Column(NVARCHAR(50), nullable=False, unique=True)

  def __init__(self, name):
    self.name = name

class Vehicle(db_base_model):
  __tablename__ = "Vehicles"
  id = Column(INTEGER, primary_key=True, autoincrement=True)
  license_plate = Column(VARCHAR(50), nullable=False, unique=True)
  vehicle_campany_id = Column(INTEGER, ForeignKey(VehicleCampany.id))
  status = Column(INTEGER, nullable=False)

  def __init__(self, license_plate, vehicle_campany_id, status):
    self.license_plate = license_plate
    self.vehicle_campany_id = vehicle_campany_id
    self.status = status

class ListVehicleDetail(db_base_model):
  __tablename__ = "ListVehicleDetail"
  id = Column(INTEGER, primary_key=True, autoincrement=True) 
  list_vehicle_id = Column(INTEGER, ForeignKey(ListVehicle.id), nullable=False)
  vehicle_id = Column(INTEGER, ForeignKey(Vehicle.id), nullable=False)

  def __init__(self, list_vehicle_id, vehicle_id):
    self.list_vehicle_id = list_vehicle_id
    self.vehicle_id = vehicle_id

class Feature(db_base_model):
  __tablename__ = "Features"
  id = Column(INTEGER, primary_key=True, autoincrement=True)
  name = Column(NVARCHAR(50), nullable=False)

  def __init__(self, name):
    self.name = name

class Record(db_base_model):
  __tablename__ = "Records"
  id = Column(INTEGER, primary_key=True, autoincrement=True) 
  camera_id = Column(INTEGER, ForeignKey(Camera.id), nullable=False)
  list_vehicle_id = Column(INTEGER, ForeignKey(ListVehicle.id), nullable=False)
  vehicle_id = Column(INTEGER, ForeignKey(Vehicle.id), nullable=False)
  time = Column(DATETIME, nullable=False)
  path = Column(NVARCHAR(100), nullable=False)

  def __init__(self, camera_id, list_vehicle_id, vehicle_id, time, path):
    self.camera_id = camera_id
    self.list_vehicle_id = list_vehicle_id
    self.vehicle_id = vehicle_id
    self.time = time
    self.path = path

class RecordDetail(db_base_model):
  __tablename__ = "RecordDetail"

  id = Column(INTEGER, primary_key=True, autoincrement=True) 
  feature_id = Column(INTEGER, ForeignKey(Feature.id),nullable=False)
  record_id = Column(INTEGER, ForeignKey(Record.id),nullable=False)

  def __init__(self, feature_id, record_id):
    self.feature_id = feature_id
    self.record_id = record_id
