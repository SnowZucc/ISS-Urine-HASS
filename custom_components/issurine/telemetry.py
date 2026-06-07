"""ISSLive telemetry definitions exposed as Home Assistant entities."""

from __future__ import annotations

# Keep this list intentionally small. The public ISSLive dictionary contains
# many raw engineering channels; Home Assistant should expose only values that
# are understandable without flight-controller context.
TELEMETRY: tuple[dict[str, object], ...] = (
    {"discipline": "ETHOS", "icon": "mdi:gauge", "name": "Crewlock Pressure", "native_unit_of_measurement": null, "numeric": true, "public_pui": "AIRLOCK000049", "source_unit": "CNT"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Hi P O2 Supply valve position", "native_unit_of_measurement": null, "numeric": false, "public_pui": "AIRLOCK000050", "source_unit": "N/A"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Lo P O2 Supply Valve position", "native_unit_of_measurement": null, "numeric": false, "public_pui": "AIRLOCK000051", "source_unit": "N/A"},
    {"discipline": "ETHOS", "icon": "mdi:gauge", "name": "Airlock Pressure", "native_unit_of_measurement": "psi", "numeric": true, "public_pui": "AIRLOCK000054", "source_unit": "PSI"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Airlock Hi P O2 Tank Pressure", "native_unit_of_measurement": null, "numeric": true, "public_pui": "AIRLOCK000055", "source_unit": "CNT"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Airlock Lo P O2 Tank Pressure", "native_unit_of_measurement": null, "numeric": true, "public_pui": "AIRLOCK000056", "source_unit": "CNT"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Node 3 ppO2", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "NODE3000001", "source_unit": "PSIA"},
    {"discipline": "ETHOS", "icon": "mdi:gauge", "name": "Node 3 ppN2", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "NODE3000002", "source_unit": "PSIA"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Node 3 ppCO2", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "NODE3000003", "source_unit": "PSIA"},
    {"discipline": "ETHOS", "icon": "mdi:water-opacity", "name": "Urine Processor State", "native_unit_of_measurement": null, "numeric": false, "public_pui": "NODE3000004", "source_unit": "N/A"},
    {"discipline": "ETHOS", "icon": "mdi:water-opacity", "name": "Urine Tank Qty", "native_unit_of_measurement": "%", "numeric": true, "public_pui": "NODE3000005", "source_unit": "PCT"},
    {"discipline": "ETHOS", "icon": "mdi:water-sync", "name": "Water Processor State", "native_unit_of_measurement": null, "numeric": false, "public_pui": "NODE3000006", "source_unit": "N/A"},
    {"discipline": "ETHOS", "icon": "mdi:water-sync", "name": "Water Processor Step", "native_unit_of_measurement": null, "numeric": false, "public_pui": "NODE3000007", "source_unit": "N/A"},
    {"discipline": "ETHOS", "icon": "mdi:water-alert", "name": "Waste Water Tank Qty", "native_unit_of_measurement": "%", "numeric": true, "public_pui": "NODE3000008", "source_unit": "PCT"},
    {"discipline": "ETHOS", "icon": "mdi:water-check", "name": "Clean Water Tank Qty", "native_unit_of_measurement": "%", "numeric": true, "public_pui": "NODE3000009", "source_unit": "PCT"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Oxygen Generator State", "native_unit_of_measurement": null, "numeric": false, "public_pui": "NODE3000010", "source_unit": "N/A"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "O2 Production rate", "native_unit_of_measurement": "lb/day", "numeric": true, "public_pui": "NODE3000011", "source_unit": "LBM/D"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Lab ppO2", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "USLAB000053", "source_unit": "PSIA"},
    {"discipline": "ETHOS", "icon": "mdi:gauge", "name": "Lab ppN2", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "USLAB000054", "source_unit": "PSIA"},
    {"discipline": "ETHOS", "icon": "mdi:molecule", "name": "Lab ppCO2", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "USLAB000055", "source_unit": "PSIA"},
    {"discipline": "ETHOS", "icon": "mdi:gauge", "name": "Cabin pressure", "native_unit_of_measurement": "mmHg", "numeric": true, "public_pui": "USLAB000058", "source_unit": "PSI"},
    {"discipline": "ETHOS", "icon": "mdi:thermometer", "name": "Cabin temperature", "native_unit_of_measurement": "°C", "numeric": true, "public_pui": "USLAB000059", "source_unit": "CNT"},
    {"discipline": "ADCO", "icon": "mdi:scale", "name": "ISS Total Mass (kg)", "native_unit_of_measurement": "kg", "numeric": true, "public_pui": "USLAB000039", "source_unit": "KG"},
    {"discipline": "VVO", "icon": "mdi:state-machine", "name": "Attitude Maneuver In Progress status", "native_unit_of_measurement": null, "numeric": false, "public_pui": "USLAB000081", "source_unit": "N/A"},
    {"discipline": "ODIN/VVO", "icon": "mdi:state-machine", "name": "ISS Station Mode", "native_unit_of_measurement": null, "numeric": false, "public_pui": "USLAB000086", "source_unit": "N/A"},
)

TELEMETRY_BY_PUI = {str(item["public_pui"]): item for item in TELEMETRY}
PUBLIC_PUIS = tuple(str(item["public_pui"]) for item in TELEMETRY)
