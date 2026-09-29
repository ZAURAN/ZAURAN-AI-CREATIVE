"""Bounded TypeSafe client. Never log credentials, evidence, or error bodies."""
import json
import os
import urllib.request

ENDPOINT = 'https://api.typesafe.ai/v1/systemone'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def api_key():
    value = os.environ.get('TYPESAFE_API_KEY', '')
    if value or os.name != 'nt':
        return value
    # A running desktop app may predate a newly configured User environment.
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as key:
            value, _ = winreg.QueryValueEx(key, 'TYPESAFE_API_KEY')
            return value if isinstance(value, str) else ''
    except OSError:
        return ''


def evaluate(payload):
    key = api_key()
    if not key:
        raise RuntimeError('TypeSafe credential unavailable')
    data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode('utf-8')
    request = urllib.request.Request(
        ENDPOINT, data=data, method='POST',
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
    )
    # One attempt only; caller decides whether a later retry is worth its cost.
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(request, timeout=15) as response:
        body = response.read(1_000_001)
    if len(body) > 1_000_000:
        raise ValueError('Response too large')
    return json.loads(body)
