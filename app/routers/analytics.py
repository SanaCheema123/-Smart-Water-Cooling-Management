from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.database import get_db
from app.db.models import SensorReading, Alert
from app.services.predictor import predict
from app.services.weather import current_weather
from app.services.recommendations import make_recommendations
from app.services.anomaly import detect

router = APIRouter(prefix="/api", tags=["Analytics"])

def latest_or_404(db):
    r = db.query(SensorReading).order_by(desc(SensorReading.timestamp)).first()
    if not r: raise HTTPException(404, "No readings yet")
    return r

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    r = latest_or_404(db)
    return {"latest": r, "active_alerts": db.query(Alert).filter(Alert.acknowledged == False).count(), "wue": wue(db)}

@router.get("/wue")
def wue(db: Session = Depends(get_db)):
    rows = db.query(SensorReading).all()
    if not rows: raise HTTPException(404, "No readings yet")
    total_water = sum(max(r.water_makeup_lph, 0) for r in rows)
    total_energy = sum(max(r.cooling_load_kw, 0) for r in rows)
    value = total_water / max(total_energy, 1e-9)
    return {"wue_liters_per_kwh": round(value, 4), "samples": len(rows), "formula": "water consumption / cooling-energy proxy"}

@router.get("/predictions/demand")
def demand(horizon: int = Query(6, ge=1, le=48), db: Session = Depends(get_db)):
    rows = db.query(SensorReading).order_by(SensorReading.timestamp.asc()).all()
    if not rows: raise HTTPException(404, "No readings yet")
    preds, confidence = predict(rows, horizon)
    return {"horizon_hours": horizon, "predicted_water_lph": preds, "confidence": confidence}

@router.get("/prediction")
def prediction(horizon: int = Query(6, ge=1, le=48), db: Session = Depends(get_db)):
    return demand(horizon, db)

@router.get("/weather")
async def weather():
    return await current_weather()

@router.get("/recommendations")
async def recommendations(db: Session = Depends(get_db)):
    latest = latest_or_404(db)
    try: w = await current_weather()
    except Exception: w = {"source":"unavailable", "temperature_c":None, "humidity_pct":None}
    return {"recommendations": make_recommendations(latest, w), "weather": w}

@router.get("/alerts")
def alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(desc(Alert.timestamp)).limit(100).all()

@router.get("/anomaly")
def anomaly(db: Session = Depends(get_db)):
    rows = db.query(SensorReading).order_by(SensorReading.timestamp.asc()).limit(500).all()
    if not rows: raise HTTPException(404, "No readings yet")
    abnormal, score = detect(rows)
    return {"anomaly": abnormal, "status": "abnormal" if abnormal else "normal", "score": score}

@router.get("/leak")
def leak(db: Session = Depends(get_db)):
    r = latest_or_404(db)
    ratio = r.water_makeup_lph / max(r.water_flow_lph, 1.0)
    detected = ratio > 0.90
    return {"leak_detected": detected, "status": "LEAK" if detected else "NORMAL", "makeup_to_flow_ratio": round(ratio, 4)}

@router.patch("/alerts/{alert_id}/acknowledge")
def acknowledge(alert_id: int, db: Session = Depends(get_db)):
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a: raise HTTPException(404, "Alert not found")
    a.acknowledged = True; db.commit(); db.refresh(a)
    return a

@router.get("/reports/sustainability")
def report(db: Session = Depends(get_db)):
    rows = db.query(SensorReading).all()
    if not rows: raise HTTPException(404, "No readings yet")
    water = sum(max(r.water_makeup_lph, 0) for r in rows)
    load = sum(max(r.cooling_load_kw, 0) for r in rows)
    return {"report":"sustainability", "samples":len(rows), "water_consumption_liters_proxy":round(water,2), "cooling_energy_kwh_proxy":round(load,2), "wue_liters_per_kwh":round(water/max(load,1e-9),4), "alerts":db.query(Alert).count()}
