from datetime import datetime
from datetime import timezone


def get_utc_now():
    return datetime.now(timezone.utc)
