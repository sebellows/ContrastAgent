from datetime import datetime, timezone

def tz_aware_utc_now():
    """Returns a timezone aware UTC datetime object."""
    return datetime.now(timezone.utc)
