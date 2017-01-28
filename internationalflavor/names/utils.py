from .data import NL_VOORVOEGSELS


def _split_name_generic(name, long_first=False, **kwargs):
    # If long_first is set, we prefer a longer first name
    if long_first:
        parts = name.rsplit(None, 1)
    else:
        parts = name.split(None, 1)
    if len(parts) == 1:
        return "", parts[0]
    else:
        return tuple(parts)


def _split_name_nl(name, **kwargs):
    vvg_matches = [(" %s " % x.lower()) for x in NL_VOORVOEGSELS if (" %s " % x.lower()) in name.lower()]
    if vvg_matches:
        vvg_match = sorted(vvg_matches, key=lambda x: (len(x), -name.lower().index(x)))[-1]
        vvg_match_idx = name.lower().index(vvg_match)
        return (name[:vvg_match_idx],
                name[vvg_match_idx + 1:vvg_match_idx + len(vvg_match) - 1],
                name[vvg_match_idx + len(vvg_match):])
    else:
        result = _split_name_generic(name, **kwargs)
        return result[0], "", result[1]


def split_name(name, scheme=None, **kwargs):
    """Splits a name in several parts. Useful for when you are working with applications that store names in separate
    parts, and with applications that don't.

    This utility method works on several schemes, the default being None, simply splitting a name. The result depends
    on the scheme you choose. Additionally, you can specify whether you want honorific titles returned. This is not
    supported by all schemes.

    .. warning::

       There is no fool-proof method to split names that works in all edge cases correctly. If you need to have names
       split, simply ask them to be entered in split form. This method is best-effort only and provides the guarantee
       that it will make mistakes.

    A scheme may support additional arguments, these are specified below.

    The following schemes are supported:

    * **None** : split a name in two parts, simply splitting on the first whitespace, ignoring honorific titles etc.
                 returns a tuple of (first_name, last_name), when the name can not be split, it is put in the last_name.

                 extra kwarg: long_first  : if set, a long first name is preferred over a long last name.

    * **NL**   : split a name in three parts, splitting including the Dutch 'voorvoegsel' or 'tussenvoegsel',
                 ignores honorific titles etc. When no such voorvoegsel exists, it falls back to the None scheme.

    Using stalemate you can set whether you prefer longer first names or longer last names.

    """

    if scheme == "NL":
        return _split_name_nl(name, **kwargs)

    return _split_name_generic(name, **kwargs)


def join_name(*parts):
    """Joins a name. This is the inverse of split_name, but x == join_name(split_name(x)) does not necessarily hold.

    Joining a name may also be subject to different schemes, but the most basic implementation is just joining all parts
    with a space.
    """
    return " ".join(parts)
