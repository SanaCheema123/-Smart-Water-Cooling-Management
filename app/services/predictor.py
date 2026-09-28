import numpy as np
from sklearn.ensemble import RandomForestRegressor

FEATURES = ["cooling_load_kw", "ambient_temp_c", "humidity_pct", "return_temp_c"]

def predict(rows, horizon=6):
    if len(rows) < 10:
        last = rows[-1].water_makeup_lph if rows else 0
        return [round(last, 2)] * horizon, 0.55
    X = np.array([[getattr(r, f) for f in FEATURES] for r in rows])
    y = np.array([r.water_makeup_lph for r in rows])
    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X, y)
    last = X[-1]
    # Prototype: near-term forecast assumes current operating conditions.
    preds = [float(model.predict([last])[0]) for _ in range(horizon)]
    return [round(max(0, p), 2) for p in preds], 0.80
