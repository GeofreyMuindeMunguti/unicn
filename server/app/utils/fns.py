from datetime import datetime


def convert_utc_to_timezone_date(date: datetime) -> datetime:
    # try:
    #     ip_info = context.data["Ip-Info"]
    #     if not ip_info:
    #         return date
    #     timezone = ip_info.location.time_zone
    #     formated_date = date.astimezone(pytz.timezone(timezone))
    #     return formated_date
    # except Exception:
    #     return date
    return date
