"""Lightstreamer client for NASA ISSLive public telemetry."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
from typing import Any
from urllib.parse import unquote

import aiohttp

from .const import (
    LIGHTSTREAMER_ADAPTER_SET,
    LIGHTSTREAMER_CLIENT_ID,
    LIGHTSTREAMER_SCHEMA,
    LIGHTSTREAMER_URL,
)

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ISSLiveTelemetryValue:
    """One decoded ISSLive telemetry value."""

    public_pui: str
    value: Any
    raw_value: str | None
    calibrated_data: str | None
    source_timestamp: str | None
    status_class: str | None
    status_indicator: str | None
    status_color: str | None


class ISSLiveApiError(Exception):
    """Raised when the ISSLive endpoint cannot return telemetry."""


class ISSLiveClient:
    """Small snapshot client for the public ISSLive Lightstreamer feed."""

    def __init__(self, session: aiohttp.ClientSession, timeout: int = 20) -> None:
        self._session = session
        self._timeout = timeout

    async def async_fetch(self, public_puis: list[str]) -> dict[str, ISSLiveTelemetryValue]:
        """Fetch a snapshot for all requested Public PUI identifiers."""

        if not public_puis:
            return {}

        item_by_position = {
            index: public_pui for index, public_pui in enumerate(public_puis, start=1)
        }
        payload = {
            "LS_adapter_set": LIGHTSTREAMER_ADAPTER_SET,
            "LS_cid": LIGHTSTREAMER_CLIENT_ID,
            "LS_op": "add",
            "LS_subId": "1",
            "LS_group": " ".join(public_puis),
            "LS_schema": " ".join(LIGHTSTREAMER_SCHEMA),
            "LS_mode": "MERGE",
            "LS_snapshot": "true",
        }

        values: dict[str, ISSLiveTelemetryValue] = {}
        buffer = ""

        try:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            async with self._session.post(
                LIGHTSTREAMER_URL, data=payload, timeout=timeout
            ) as response:
                response.raise_for_status()
                async with asyncio.timeout(self._timeout):
                    async for chunk in response.content.iter_chunked(8192):
                        buffer += chunk.decode("utf-8", "replace")
                        lines = buffer.splitlines(keepends=True)

                        if lines and not lines[-1].endswith(("\n", "\r")):
                            buffer = lines.pop()
                        else:
                            buffer = ""

                        for line in lines:
                            self._parse_line(line.strip(), item_by_position, values)

                        if len(values) >= len(public_puis):
                            return values
        except (aiohttp.ClientError, TimeoutError, asyncio.TimeoutError) as err:
            if values:
                _LOGGER.debug(
                    "ISSLive snapshot timed out after %s/%s values",
                    len(values),
                    len(public_puis),
                )
                return values
            raise ISSLiveApiError("Unable to fetch ISSLive telemetry") from err

        if not values:
            raise ISSLiveApiError("ISSLive returned no telemetry values")

        return values

    @staticmethod
    def _parse_line(
        line: str,
        item_by_position: dict[int, str],
        values: dict[str, ISSLiveTelemetryValue],
    ) -> None:
        """Parse one TLCP update line."""

        if not line.startswith("U,"):
            return

        parts = line.split(",", 3)
        if len(parts) != 4:
            return

        try:
            item_position = int(parts[2])
        except ValueError:
            return

        public_pui = item_by_position.get(item_position)
        if public_pui is None or public_pui in values:
            return

        fields = parts[3].split("|")
        if len(fields) < len(LIGHTSTREAMER_SCHEMA):
            fields.extend([""] * (len(LIGHTSTREAMER_SCHEMA) - len(fields)))

        if any(field.startswith("^") for field in fields):
            return

        source_timestamp, raw_value, status_class, status_indicator, status_color, calibrated = (
            field or None for field in fields[:6]
        )
        decoded_color = unquote(status_color) if status_color else None
        state = _coerce_value(calibrated or raw_value)

        values[public_pui] = ISSLiveTelemetryValue(
            public_pui=public_pui,
            value=state,
            raw_value=raw_value,
            calibrated_data=calibrated,
            source_timestamp=source_timestamp,
            status_class=status_class,
            status_indicator=status_indicator,
            status_color=decoded_color,
        )


def _coerce_value(value: str | None) -> Any:
    """Convert numeric telemetry strings while preserving enum labels."""

    if value is None or value == "":
        return None

    try:
        number = float(value)
    except ValueError:
        return value

    if number.is_integer() and "." not in value:
        return int(number)
    return number
