"""Sensors for ISS urine Telemetry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ISSLiveDataUpdateCoordinator
from .const import (
    ATTR_CALIBRATED_DATA,
    ATTR_DISCIPLINE,
    ATTR_PUBLIC_PUI,
    ATTR_RAW_VALUE,
    ATTR_SOURCE_TIMESTAMP,
    ATTR_STATUS_CLASS,
    ATTR_STATUS_COLOR,
    ATTR_STATUS_INDICATOR,
    DOMAIN,
)
from .telemetry import TELEMETRY


@dataclass(frozen=True, kw_only=True)
class ISSLiveSensorEntityDescription(SensorEntityDescription):
    """Description for an ISSLive sensor."""

    public_pui: str
    discipline: str
    source_unit: str | None = None
    numeric: bool = False


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up ISS urine Telemetry sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ISSLiveTelemetrySensor(
            coordinator,
            ISSLiveSensorEntityDescription(
                key=str(item["public_pui"]).lower(),
                name=str(item["name"]),
                public_pui=str(item["public_pui"]),
                discipline=str(item["discipline"]),
                native_unit_of_measurement=_normalize_unit(
                    item.get("native_unit_of_measurement")
                ),
                icon=str(item["icon"]),
                source_unit=(
                    str(item["source_unit"]) if item.get("source_unit") else None
                ),
                numeric=bool(item["numeric"]),
            ),
        )
        for item in TELEMETRY
    )


class ISSLiveTelemetrySensor(
    CoordinatorEntity[ISSLiveDataUpdateCoordinator], SensorEntity
):
    """One ISSLive telemetry sensor."""

    entity_description: ISSLiveSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ISSLiveDataUpdateCoordinator,
        description: ISSLiveSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.public_pui.lower()}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "issurine")},
            name="ISS urine Telemetry",
            manufacturer="NASA / Lightstreamer",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> Any:
        """Return the sensor state."""

        value = self.coordinator.data.get(self.entity_description.public_pui)
        if value is None:
            return None
        return value.value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra telemetry metadata."""

        telemetry = self.coordinator.data.get(self.entity_description.public_pui)
        attrs: dict[str, Any] = {
            ATTR_PUBLIC_PUI: self.entity_description.public_pui,
            ATTR_DISCIPLINE: self.entity_description.discipline,
        }
        if self.entity_description.source_unit:
            attrs["source_unit"] = self.entity_description.source_unit
        if telemetry is None:
            return attrs

        attrs.update(
            {
                ATTR_RAW_VALUE: telemetry.raw_value,
                ATTR_CALIBRATED_DATA: telemetry.calibrated_data,
                ATTR_SOURCE_TIMESTAMP: telemetry.source_timestamp,
                ATTR_STATUS_CLASS: telemetry.status_class,
                ATTR_STATUS_INDICATOR: telemetry.status_indicator,
                ATTR_STATUS_COLOR: telemetry.status_color,
            }
        )
        return attrs

    @property
    def available(self) -> bool:
        """Return true if the telemetry value exists."""

        return (
            super().available
            and self.entity_description.public_pui in self.coordinator.data
        )


def _normalize_unit(unit: object | None) -> str | None:
    """Normalize units for Home Assistant display."""

    if unit is None:
        return None
    if unit == "%":
        return PERCENTAGE
    return str(unit)
