import time, datetime, calendar
import urllib.request, urllib.error

class URLError(Exception):
    pass

def time_since_epoch():
    return calendar.timegm(time.gmtime())

def open_url(url):
    try:
        return urllib.request.urlopen(url).read().decode("utf-8")
    except urllib.error.URLError:
        raise URLError
