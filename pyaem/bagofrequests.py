import cStringIO
from .handlers import unexpected as handle_unexpected
import pycurl
import urllib

def request(method, url, params, handlers, **kwargs):

    curl = pycurl.Curl()
    body_io = cStringIO.StringIO()

    if method == 'post':
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(params, True))
    elif method == 'delete':
        curl.setopt(pycurl.CUSTOMREQUEST, method)
    else:
        url = '{0}?{1}'.format(url, urllib.urlencode(params, True))

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.WRITEFUNCTION, body_io.write)

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': body_io.getvalue(),
        'request': {
            'method': method,
            'url': url,
            'params': params
        }
    }

    curl.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response, **kwargs)


def download_file(url, params, handlers, **kwargs):

    curl = pycurl.Curl()
    body_io = cStringIO.StringIO()
    url = '{0}?{1}'.format(url, urllib.urlencode(params, True))
    data = open(kwargs['file'], 'wb')

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.WRITEDATA, data)
    curl.setopt(pycurl.WRITEFUNCTION, body_io.write)

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': body_io.getvalue(),
        'request': {
            'method': 'get',
            'url': url,
            'params': params
        }
    }

    curl.close()
    data.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response, **kwargs)


def upload_file(url, params, handlers, **kwargs):

    curl = pycurl.Curl()
    body_io = cStringIO.StringIO()
    _params = []
    for key, value in params.iteritems():
        _params.append((key, value))

    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.HTTPPOST, _params)
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.WRITEFUNCTION, body_io.write)

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': body_io.getvalue(),
        'request': {
            'method': 'post',
            'url': url,
            'params': params
        }
    }

    curl.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response, **kwargs)
