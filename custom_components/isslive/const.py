"""Constants for the ISS Live Telemetry integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "isslive"

DEFAULT_SCAN_INTERVAL = 60
MIN_SCAN_INTERVAL = 30
MAX_SCAN_INTERVAL = 3600

CONF_SCAN_INTERVAL = "scan_interval"

PLATFORMS = ["sensor"]

DEFAULT_UPDATE_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

LIGHTSTREAMER_URL = (
    "https://push.lightstreamer.com/lightstreamer/create_session.txt"
    "?LS_protocol=TLCP-2.5.0"
)
LIGHTSTREAMER_ADAPTER_SET = "ISSLIVE"
LIGHTSTREAMER_CLIENT_ID = "mgQkwtwdysogQz2BJ4Ji kOj2Bg"
LIGHTSTREAMER_SCHEMA = (
    "TimeStamp",
    "Value",
    "Status.Class",
    "Status.Indicator",
    "Status.Color",
    "CalibratedData",
)

ATTR_PUBLIC_PUI = "public_pui"
ATTR_DISCIPLINE = "discipline"
ATTR_RAW_VALUE = "raw_value"
ATTR_CALIBRATED_DATA = "calibrated_data"
ATTR_SOURCE_TIMESTAMP = "source_timestamp"
ATTR_STATUS_CLASS = "status_class"
ATTR_STATUS_INDICATOR = "status_indicator"
ATTR_STATUS_COLOR = "status_color"
