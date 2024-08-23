LOG_PATTERN = (
    r'{"time": "(?P<time>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})", '
    r'"remote_ip": "(?P<remote_ip>\S+)", '
    r'"remote_user": "(?P<remote_user>\S+)", '
    r'"request": "(?P<method>\S+) (?P<uri>\S+) HTTP/\d\.\d", '
    r'"response": (?P<response>\d+), '
    r'"bytes": (?P<bytes>\d+), '
    r'"referrer": "(?P<referrer>\S+)", '
    r'"agent": "(?P<agent>.+?)"}'
)
