"""Constants for the Hangzhou Ranqi integration."""

from datetime import timedelta

DOMAIN = "hangzhou_ranqi"

CONF_USER_NUMBER = "user_number"
CONF_ADDRESS = "address"

DEFAULT_SCAN_INTERVAL = timedelta(hours=2)

API_BASE_URL = "https://ht-service.hzgas.cn"
USER_BASE_INFO_PATH = "/OnlineService/transferSystem/userBaseInfo"
QUERY_METER_DATE_PATH = "/OnlineService/transferSystem/queryMeterDate"

ATTR_ADDRESS = "address"
ATTR_METER_NO = "meter_no"
ATTR_READING = "reading"
ATTR_USE_TIME = "use_time"
ATTR_USER_NUMBER = "user_number"
