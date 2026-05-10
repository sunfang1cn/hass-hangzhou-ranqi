"""Sensor platform for Hangzhou Ranqi."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_ADDRESS,
    ATTR_METER_NO,
    ATTR_READING,
    ATTR_USE_TIME,
    ATTR_USER_NUMBER,
    DOMAIN,
)
from .coordinator import HangzhouRanqiDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hangzhou Ranqi sensors from a config entry."""
    coordinator: HangzhouRanqiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            HangzhouRanqiDailyUsageSensor(coordinator, entry),
            HangzhouRanqiCurrentReadingSensor(coordinator, entry),
        ]
    )


class HangzhouRanqiDailyUsageSensor(CoordinatorEntity[HangzhouRanqiDataUpdateCoordinator], SensorEntity):
    """Latest daily gas usage sensor."""

    _attr_device_class = SensorDeviceClass.GAS
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "daily_usage"

    def __init__(
        self,
        coordinator: HangzhouRanqiDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.unique_id}_daily_usage"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(entry.unique_id))},
            "name": entry.title,
            "manufacturer": "杭州天然气有限公司",
        }

    @property
    def native_value(self) -> float | None:
        """Return the latest daily usage."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.usage

    @property
    def extra_state_attributes(self) -> dict[str, str | float] | None:
        """Return extra attributes for the latest row."""
        data = self.coordinator.data
        if data is None:
            return None

        return {
            ATTR_USE_TIME: data.use_time,
            ATTR_READING: data.reading,
            ATTR_METER_NO: data.meter_no,
            ATTR_ADDRESS: data.address,
            ATTR_USER_NUMBER: data.user_number,
        }


class HangzhouRanqiCurrentReadingSensor(CoordinatorEntity[HangzhouRanqiDataUpdateCoordinator], SensorEntity):
    """Latest gas meter reading sensor."""

    _attr_device_class = SensorDeviceClass.GAS
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_translation_key = "current_reading"

    def __init__(
        self,
        coordinator: HangzhouRanqiDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.unique_id}_current_reading"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(entry.unique_id))},
            "name": entry.title,
            "manufacturer": "杭州天然气有限公司",
        }

    @property
    def native_value(self) -> float | None:
        """Return the latest meter reading."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.reading

    @property
    def extra_state_attributes(self) -> dict[str, str | float] | None:
        """Return extra attributes for the latest row."""
        data = self.coordinator.data
        if data is None:
            return None

        return {
            ATTR_USE_TIME: data.use_time,
            ATTR_METER_NO: data.meter_no,
            ATTR_ADDRESS: data.address,
            ATTR_USER_NUMBER: data.user_number,
        }
