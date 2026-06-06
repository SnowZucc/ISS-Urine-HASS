"""Home Assistant integration for ISS urine Telemetry."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ISSLiveApiError, ISSLiveClient, ISSLiveTelemetryValue
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, PLATFORMS
from .telemetry import PUBLIC_PUIS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ISS urine Telemetry from a config entry."""

    scan_interval = int(entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    client = ISSLiveClient(async_get_clientsession(hass))
    coordinator = ISSLiveDataUpdateCoordinator(
        hass=hass,
        client=client,
        public_puis=list(PUBLIC_PUIS),
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload ISS urine Telemetry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


class ISSLiveDataUpdateCoordinator(
    DataUpdateCoordinator[dict[str, ISSLiveTelemetryValue]]
):
    """Coordinator for shared ISSLive polling."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: ISSLiveClient,
        public_puis: list[str],
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name="ISS urine Telemetry",
            update_interval=update_interval,
        )
        self.client = client
        self.public_puis = public_puis

    async def _async_update_data(self) -> dict[str, ISSLiveTelemetryValue]:
        """Fetch latest telemetry."""

        try:
            return await self.client.async_fetch(self.public_puis)
        except ISSLiveApiError as err:
            raise UpdateFailed(str(err)) from err
