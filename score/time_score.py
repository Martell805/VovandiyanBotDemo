from datetime import datetime, timedelta, timezone


def get_current_time_msk() -> datetime:
    delta = timedelta(hours=3, minutes=0)
    utc_time = datetime.now(timezone.utc)
    return utc_time + delta


def get_fine_current_time_msk() -> str:
    return f'{get_current_time_msk():%d-%m-%Y %H:%M:%S}'


def get_current_score_msk() -> int:
    return int(datetime.timestamp(get_current_time_msk()))
