from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.database import get_db
from app.db.models import SensorReading, Alert
from app.schemas import SensorReadingIn, SensorReadingOut
from app.services.broadcast import broadcast
from app.services.anomaly import detect

router = APIRouter(prefix="/api/readings", tags=["Sensors"])

@router.post("", response_model=SensorReadingOut)
async def create_reading(payload: SensorReadingIn, db: Session = Depends(get_db)):
    r = SensorReading(**payload.model_dump(exclude_none=True))
    if r.timestamp is None:
        r.timestamp = datetime.utcnow()
    db.add(r); db.commit(); db.refresh(r)
    rows = db.query(SensorReading).order_by(SensorReading.timestamp.asc()).limit(500).all()
    abnormal, score = detect(rows)
    alerts = []
    flow_ratio = r.water_makeup_lph / max(r.water_flow_lph, 1.0)
    if flow_ratio > 0.90:
        alerts.append(Alert(alert_type="leak", severity="critical", message="Possible cooling-water leak or abnormal makeup-water consumption detected.", value=r.water_makeup_lph))
    if r.tank_level_pct < 15:
        alerts.append(Alert(alert_type="low_tank_level", severity="high", message="Cooling-water tank level is critically low.", value=r.tank_level_pct))
    if r.return_temp_c - r.supply_temp_c > 15 or r.return_temp_c > 40:
        alerts.append(Alert(alert_type="thermal_anomaly", severity="high", message="Cooling return temperature is outside the safe prototype threshold.", value=r.return_temp_c))
    if abnormal and not alerts:
        alerts.append(Alert(alert_type="water_anomaly", severity="high", message="Abnormal cooling-water operating pattern detected.", value=r.water_makeup_lph))
    for a in alerts: db.add(a)
    db.commit()
    for a in alerts: db.refresh(a)
    await broadcast({"type":"sensor_reading", "reading":SensorReadingOut.model_validate(r).model_dump(mode="json"), "alerts":[{"id":a.id,"type":a.alert_type,"severity":a.severity,"message":a.message} for a in alerts], "anomaly_score":score})
    return r

@router.get("", response_model=list[SensorReadingOut])
def readings(limit: int = 100, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 1000))
    return db.query(SensorReading).order_by(desc(SensorReading.timestamp)).limit(limit).all()

@router.get("/latest", response_model=SensorReadingOut)
def latest(db: Session = Depends(get_db)):
    r = db.query(SensorReading).order_by(desc(SensorReading.timestamp)).first()
    if not r: raise HTTPException(404, "No sensor readings yet")
    return r
