from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean, Text
from app.db.database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    water_flow_lph = Column(Float, nullable=False)
    water_makeup_lph = Column(Float, nullable=False)
    cooling_load_kw = Column(Float, nullable=False)
    supply_temp_c = Column(Float, nullable=False)
    return_temp_c = Column(Float, nullable=False)
    ambient_temp_c = Column(Float, nullable=False)
    humidity_pct = Column(Float, nullable=False)
    tank_level_pct = Column(Float, nullable=False)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    value = Column(Float, nullable=True)
    acknowledged = Column(Boolean, default=False)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    horizon_hours = Column(Integer, nullable=False)
    predicted_water_lph = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
