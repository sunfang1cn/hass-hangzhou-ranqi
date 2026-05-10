"""Config flow for Hangzhou Ranqi."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import HangzhouRanqiAuthError, HangzhouRanqiClient, HangzhouRanqiError
from .const import CONF_ADDRESS, CONF_USER_NUMBER, DOMAIN


class HangzhouRanqiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hangzhou Ranqi."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            user_number = user_input[CONF_USER_NUMBER].strip()
            address = user_input[CONF_ADDRESS].strip()

            client = HangzhouRanqiClient(
                async_get_clientsession(self.hass),
                user_number,
                address,
            )

            try:
                await client.async_validate()
            except HangzhouRanqiAuthError:
                errors["base"] = "invalid_auth"
            except HangzhouRanqiError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_number)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"杭州燃气 {address}",
                    data={
                        CONF_USER_NUMBER: user_number,
                        CONF_ADDRESS: address,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USER_NUMBER): str,
                    vol.Required(CONF_ADDRESS): str,
                }
            ),
            errors=errors,
        )
