import re
from uuid import UUID


def validate_uuid4(uuid: str) -> bool:
    """validate_uuid4 is used to check if given string
    is valid uuid4 string.

    Args:
        uuid (str): uuid4 string to check

    Returns:
        Union(str, None): returns valid string and if not valid, returns None
    """
    pattern = re.compile(
        r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$')

    if not isinstance(uuid, str):
        if isinstance(uuid, UUID):
            uuid = str(uuid)
        else:
            return False
    check = pattern.match(uuid)
    return True if check else False


def validate_flags(flags: str) -> bool:
    pattern = re.compile(r'(.*;)*')
    if not isinstance(flags, str):
        return False

    check = pattern.match(flags)
    if check:
        return check.end(0) == len(flags)
    return False
