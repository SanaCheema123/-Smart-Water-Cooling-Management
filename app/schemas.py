from datetime import datetime
from pydantic import BaseModel, Field

class SensorReadingIn(BaseModel):
    timestamp: datetime | None = None
    water_flow_lph: float = Field(gt=0)
    water_makeup_lph: float = Field(gt=0)
    cooling_load_kw: float = Field(ge=0)
    supply_temp_c: float
    return_temp_c: float
    ambient_temp_c: float
    humidity_pct: float = Field(ge=0, le=100)
    tank_level_pct: float = Field(ge=0, le=100)

class SensorReadingOut(SensorReadingIn):
    id: int
    timestamp: datetime
    model_config = {"from_attributes": True}

class AlertOut(BaseModel):
    id: int
    timestamp: datetime
    alert_type: str
    severity: str
    message: str
    value: float | None
    acknowledged: bool
    model_config = {"from_attributes": True}
