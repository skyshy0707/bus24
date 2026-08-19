import datetime


def now(tzinfo=None):
    return datetime.datetime.now(tz=tzinfo)