# -*- coding: utf-8 -*-

def to_base(q, alphabet):
    """Calculates a change base given an alphabet"""
    if q < 0:
        raise ValueError, "first parameter must be positive integer"
    l = len(alphabet)
    converted = []
    while q != 0:
        q, r = divmod(q, l)
        converted.insert(0, alphabet[r])
    return "".join(converted) or '0'

def create_url_id(id):
    """
    Returns a encoded string for a given number.
    It adds an offset to ensure there is a decent sized result
    """
    offset = 10000000
    return to_base(offset + id, 'n5f4kcrupwbd8ez69x7gs3t2jhmyvaq')

