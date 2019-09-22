from dateutil.tz import tzutc, gettz, tzoffset


def get_timezone(tzname, offset=None):
    """
    Returns timezone from string.
    :param tzname:
        timezone name ('Europe/Vienna') or offset ('GMT+02:00' or '+2:00').
        Ignored is offset provived
    :param offset:
        timezone offset from UTC in seconds.
    :return: timezone object
    """
    if offset is not None:
        return tzoffset(tzname, offset)
    else:
        if tzname[0] in '+-0123456789':
            tzname = 'GMT' + tzname
        tz = gettz(tzname)
        if tz is not None:
            return tz
        raise ValueError(f'Unknown timezone: {tzname}')


def convert_to_tz(time, tz):
    """
    Accepts time (in UTC) and converts it to local time in timezone tz
    :param time: datetime object without timezone (always considered as time in UTC)
    :param tz: tzinfo object
    :return: datetime object in local time. Usually it is different from given time
    """
    return time.replace(tzinfo=tzutc()).astimezone(tz)
