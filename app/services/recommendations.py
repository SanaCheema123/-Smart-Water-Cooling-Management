def make_recommendations(latest, weather=None):
    recs = []
    if latest.return_temp_c - latest.supply_temp_c > 10:
        recs.append("Review cooling setpoints and heat-exchanger performance; temperature delta is high.")
    if latest.tank_level_pct < 25:
        recs.append("Tank level is low; verify makeup-water supply and cooling demand.")
    if latest.water_flow_lph > latest.water_makeup_lph * 1.8:
        recs.append("Water flow is high relative to makeup demand; inspect valves and circulation losses.")
    if weather and weather.get("temperature_c") is not None:
        if weather["temperature_c"] > 35:
            recs.append("Hot weather: pre-cool or increase cooling capacity gradually and monitor water demand.")
        elif weather["temperature_c"] < 20:
            recs.append("Cool weather: consider reducing cooling intensity while maintaining safe equipment limits.")
    if not recs:
        recs.append("Operating conditions look normal. Continue monitoring and maintain current safe setpoints.")
    return recs
