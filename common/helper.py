def get_cookies(scope):
    headers = {key: value for key, value in scope['headers']}
    cookie_header = headers.get(b'cookie', b'')
    cookie_string = cookie_header.decode('utf-8')
    cookies = {}
    for cookie in cookie_string.split(';'):
        if '=' in cookie:
            name, value = cookie.strip().split('=', 1)
            cookies[name] = value

    return cookies
