from dateutil.tz import tzutc, gettz, tzoffset


def parse_time(min_offset):
    hours, minutes = divmod(abs(min_offset), 60)
    sign = '+' if min_offset >= 0 else '-'
    return f'{sign}{hours:02d}:{minutes:02d}'


def get_timezone(tzname='UTC'):
    """
    Returns timezone from string.
    :param tzname:
        timezone name ('Europe/Vienna') or offset ('GMT+02:00' or '+2:00')
        or timezone offset from UTC in minutes.
    :return: timezone object
    """
    if isinstance(tzname, int):
        return tzoffset('GMT' + parse_time(tzname), 60 * tzname)
    else:
        if tzname == 'UTC':
            return tzutc()
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
