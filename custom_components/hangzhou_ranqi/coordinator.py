"""Data update coordinator for Hangzhou Ranqi."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import HangzhouRanqiClient, HangzhouRanqiDailyUsage, HangzhouRanqiError
from .const import CONF_ADDRESS, CONF_USER_NUMBER, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HangzhouRanqiDataUpdateCoordinator(DataUpdateCoordinator[HangzhouRanqiDailyUsage]):
    """Coordinator for Hangzhou Ranqi daily usage data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.client = HangzhouRanqiClient(
            async_get_clientsession(hass),
            entry.data[CONF_USER_NUMBER],
            entry.data[CONF_ADDRESS],
        )

    async def _async_update_data(self) -> HangzhouRanqiDailyUsage:
        """Fetch data from the API."""
        try:
            return await self.client.async_get_latest_usage(dt_util.now().date())
        except HangzhouRanqiError as err:
            raise UpdateFailed(str(err)) from err
