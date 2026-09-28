import numpy as np
from sklearn.ensemble import IsolationForest

FEATURES = ["water_flow_lph", "water_makeup_lph", "cooling_load_kw", "supply_temp_c", "return_temp_c", "ambient_temp_c", "humidity_pct", "tank_level_pct"]

def detect(rows):
    if not rows:
        return False, 0.0
    latest = rows[-1]
    # Deterministic safety rules are checked before ML so obvious leaks/unsafe states are caught.
    flow_ratio = latest.water_makeup_lph / max(latest.water_flow_lph, 1.0)
    temp_delta = latest.return_temp_c - latest.supply_temp_c
    if flow_ratio > 0.90 or latest.tank_level_pct < 15 or temp_delta > 15 or latest.return_temp_c > 40:
        return True, -1.0
    if len(rows) < 20:
        return False, 0.0
    X = np.array([[getattr(r, f) for f in FEATURES] for r in rows])
    model = IsolationForest(contamination=0.05, random_state=42, n_estimators=150)
    model.fit(X)
    score = float(model.decision_function(X[-1:])[0])
    return bool(model.predict(X[-1:])[0] == -1), score
