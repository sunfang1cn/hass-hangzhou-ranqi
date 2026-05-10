"""Client for Hangzhou Ranqi daily gas usage data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import API_BASE_URL, QUERY_METER_DATE_PATH, USER_BASE_INFO_PATH


class HangzhouRanqiError(Exception):
    """Base error for Hangzhou Ranqi API failures."""


class HangzhouRanqiAuthError(HangzhouRanqiError):
    """Raised when the user number cannot be resolved."""


@dataclass(frozen=True)
class HangzhouRanqiDailyUsage:
    """Latest daily gas usage reading."""

    user_number: str
    address: str
    meter_no: str
    use_time: str
    reading: float
    usage: float


class HangzhouRanqiClient:
    """Small async client for the Hangzhou Ranqi web API."""

    def __init__(self, session: ClientSession, user_number: str, address: str) -> None:
        """Initialize the client."""
        self._session = session
        self._user_number = user_number
        self._configured_address = address

    async def async_get_latest_usage(
        self,
        today: date | None = None,
    ) -> HangzhouRanqiDailyUsage:
        """Fetch the latest daily usage row for this user."""
        base_info = await self._async_get_user_base_info()
        meter_no = self._extract_meter_no(base_info)
        api_address = base_info.get("addrDes") or base_info.get("addrshortdes")
        address = str(api_address or self._configured_address)

        rows = await self._async_get_daily_usage_rows(meter_no, today or date.today())
        if not rows:
            raise HangzhouRanqiError("No daily usage rows returned")

        latest = max(rows, key=lambda row: str(row.get("useTime", "")))

        try:
            use_time = str(latest["useTime"])
            reading = float(latest["reading"])
            usage = float(latest["usage"])
        except (KeyError, TypeError, ValueError) as err:
            raise HangzhouRanqiError("Daily usage row is missing expected fields") from err

        return HangzhouRanqiDailyUsage(
            user_number=self._user_number,
            address=address,
            meter_no=meter_no,
            use_time=use_time,
            reading=reading,
            usage=usage,
        )

    async def async_validate(self) -> None:
        """Validate that the configured user number has a supported meter."""
        base_info = await self._async_get_user_base_info()
        self._extract_meter_no(base_info)

    async def _async_get_user_base_info(self) -> dict[str, Any]:
        payload = await self._async_get_json(
            USER_BASE_INFO_PATH,
            {"userNo": self._user_number},
        )
        if str(payload.get("status")) != "200":
            raise HangzhouRanqiAuthError(str(payload.get("message") or "Invalid user number"))

        data = payload.get("data")
        if not isinstance(data, dict):
            raise HangzhouRanqiAuthError("User base info not found")

        return data

    async def _async_get_daily_usage_rows(
        self,
        meter_no: str,
        today: date,
    ) -> list[dict[str, Any]]:
        start_day = today - timedelta(days=7)
        payload = await self._async_get_json(
            QUERY_METER_DATE_PATH,
            {
                "meterNo": meter_no,
                "startTime": start_day.isoformat(),
                "endTime": today.isoformat(),
                "limit": "7",
            },
        )
        if str(payload.get("status")) != "200":
            raise HangzhouRanqiError(str(payload.get("message") or "Unable to fetch daily usage"))

        data = payload.get("data")
        if not isinstance(data, list):
            raise HangzhouRanqiError("Daily usage response did not contain a data list")

        return [row for row in data if isinstance(row, dict)]

    async def _async_get_json(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        url = f"{API_BASE_URL}{path}"
        try:
            response = await self._session.get(url, params=params, timeout=20)
            response.raise_for_status()
            payload = await response.json(content_type=None)
        except (ClientError, ClientResponseError, TimeoutError) as err:
            raise HangzhouRanqiError(f"Request failed: {err}") from err

        if not isinstance(payload, dict):
            raise HangzhouRanqiError("API response was not a JSON object")

        return payload

    @staticmethod
    def _extract_meter_no(base_info: dict[str, Any]) -> str:
        meter_about = base_info.get("meterAbout")
        if not isinstance(meter_about, list):
            raise HangzhouRanqiAuthError("Meter list not found")

        for meter in meter_about:
            if not isinstance(meter, dict):
                continue
            if str(meter.get("meterType")) == "11":
                continue
            meter_no = meter.get("meterNo")
            if meter_no:
                return str(meter_no)

        raise HangzhouRanqiAuthError("No supported NB gas meter found")
