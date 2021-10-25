import re
from typing import Union


def validate_uuid4(uuid: str) -> Union[str, None]:
    """validate_uuid4 is used to check if given string
    is valid uuid4 string.

    Args:
        uuid (str): uuid4 string to check

    Returns:
        Union(str, None): returns valid string and if not valid, returns None
    """
    pattern = re.compile(
        r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$')

    if not uuid:
        return None

    if pattern.match(uuid):
        return uuid
    return None


def validate_flags(flags: str) -> bool:
    pattern = re.compile(r'(.*;)*')
    if not flags:
        return False

    check = pattern.match(flags)
    if check:
        return check.end(0) == len(flags)
    return False
