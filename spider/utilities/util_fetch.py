# _*_ coding: utf-8 _*_

"""
util_fetch.py by xianhu
"""

import random
from .util_config import CONFIG_USERAGENT_PC, CONFIG_USERAGENT_PHONE, CONFIG_USERAGENT_ALL

__all__ = [
    "make_random_useragent",
]


def make_random_useragent(ua_type="pc"):
    """
    make a random user_agent based on ua_type, ua_type can be "pc", "phone" or "all"
    """
    assert ua_type in ("pc", "phone", "all"), "make_random_useragent: ua_type is invalid"
    return random.choice(CONFIG_USERAGENT_PC if ua_type == "pc" else (CONFIG_USERAGENT_PHONE if ua_type == "phone" else CONFIG_USERAGENT_ALL))
