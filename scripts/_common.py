COUNTRY_ALTERNATIVE_KEYS = {'HK': 'HK-alt-short', 'MO': 'MO-alt-short', 'PS': 'PS-alt-short'}
TIMEZONE_TERRITORY_KEYS = {
    'Africa': '002',
    'America': '019',
    'Antarctica': 'AQ',
    'Arctic': '001',  # world
    'Asia': '142',
    'Atlantic': '001',  # world
    'Australia': '009',  # oceania
    'Etc': '001',  # world
    'Europe': '150',
    'Indian': '001',  # world
    'Pacific': '001'  # world
}


def update(d, u):
    """Method to update a dict recursively, from https://stackoverflow.com/questions/3232943/"""
    for k, v in u.items():
        if isinstance(v, dict):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def get_from_path(d, path):
    if not path:
        return d
    else:
        return get_from_path(d[path[0]], path[1:])


def _get_tz_info(region_path, rest):
    """Method that recursively diggs through the timezones variable looking for examplarCity."""

    if 'exemplarCity' in rest:
        city = rest['exemplarCity']
        return [(region_path, city)]
    elif 'short' in rest or 'long' in rest:
        return [(region_path, region_path[-1])]
    else:
        result = []
        for path, region in sorted(rest.items()):
            result.extend(_get_tz_info(region_path + [path], region))
        return result


def get_tz_info(timezones):
    result = {}
    for region_name, rest in timezones.items():
        for region_path, city in _get_tz_info([region_name], rest):
            result['/'.join(region_path)] = (region_name, city)
    return result


def _capitalize(lc):
    return lc[0:3] + lc[3:].upper().replace("LATN", "Latn").replace("HANS", "Hans").replace("HANT", "Hant")


def get_cldr_language(lc):
    if lc == 'pt-br':
        cldr_lc = 'pt'
    else:
        cldr_lc = _capitalize(lc)
    return cldr_lc


def get_locale_name(lc):
    return _capitalize(lc).replace("-", "_")
