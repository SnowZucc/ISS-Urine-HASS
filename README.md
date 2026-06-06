# ISS urine Telemetry for Home Assistant

Custom Home Assistant integration for public ISS telemetry exposed by the
Lightstreamer `ISSLIVE` adapter.

No API key is required. The integration polls:

```text
https://push.lightstreamer.com
adapter set: ISSLIVE
```

## What It Exposes

The integration intentionally exposes only the ISSLive telemetry that is useful
and understandable in Home Assistant. It creates 25 `sensor` entities.

The full ISSLive dictionary has 298 public telemetry symbols, but most are raw
engineering channels and are kept only as reference data in `data/`.

## HACS Installation

1. In HACS, add `https://github.com/SnowZucc/ISS-Urine-HASS` as a custom repository.
2. Select category `Integration`.
3. Install `ISS urine Telemetry`.
4. Restart Home Assistant.
5. Add the integration from **Settings > Devices & services > Add integration**.

Exposed sensors:

- `AIRLOCK000049` - Crewlock Pressure
- `AIRLOCK000050` - Hi P O2 Supply valve position
- `AIRLOCK000051` - Lo P O2 Supply Valve position
- `AIRLOCK000054` - Airlock Pressure
- `AIRLOCK000055` - Airlock Hi P O2 Tank Pressure
- `AIRLOCK000056` - Airlock Lo P O2 Tank Pressure
- `NODE3000001` - Node 3 ppO2
- `NODE3000002` - Node 3 ppN2
- `NODE3000003` - Node 3 ppCO2
- `NODE3000004` - Urine Processor State
- `NODE3000005` - Urine Tank Qty
- `NODE3000006` - Water Processor State
- `NODE3000007` - Water Processor Step
- `NODE3000008` - Waste Water Tank Qty
- `NODE3000009` - Clean Water Tank Qty
- `NODE3000010` - Oxygen Generator State
- `NODE3000011` - O2 Production rate
- `USLAB000053` - Lab ppO2
- `USLAB000054` - Lab ppN2
- `USLAB000055` - Lab ppCO2
- `USLAB000058` - Cabin pressure
- `USLAB000059` - Cabin temperature
- `USLAB000039` - ISS Total Mass
- `USLAB000081` - Attitude Maneuver In Progress status
- `USLAB000086` - ISS Station Mode

## Manual Installation

Copy `custom_components/issurine` into your Home Assistant
`custom_components` directory, then restart Home Assistant.

## Data Source

Source project:
https://github.com/Lightstreamer/Lightstreamer-example-ISSLive-client-javascript

Telemetry dictionary:
https://github.com/Lightstreamer/Lightstreamer-example-ISSLive-client-javascript/blob/master/src/assets/PUIList.xml
