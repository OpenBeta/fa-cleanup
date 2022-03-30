import re

def parse_fa(value):
    result = {
        'climbers': [],
        'year': None,
        'month': None,
        'day': None,
        'equipped': None,
        'needs_manual_review': None,
        'unknown_expression': False,
        'unsure': False,
    }

    for word in ('unknown', 'n/a'):
        if word in value:
            result['needs_manual_review'] = True
            return result

    if value[-1] == '?':
        result['unsure'] = True
        value = value[:-1]

    # support here abbreviated names/last names (e.g. "m. black")
    person_name_expr = '([a-z]+ [a-z]+)'
    year_expr = '([0-9]{4})'
    date_expr = f'([0-9]+)/([0-9]+)/{year_expr}'
    
    match = re.search(f'^{person_name_expr}$', value)
    if match:
        result['climbers'].append(match.group(1))
        return result

    match = re.search(f'^{year_expr}$', value)
    if match:
        result['year'] = match.group(1)
        return result

    match = re.search(f'^{person_name_expr},? {year_expr}$', value)
    if match:
        result['climbers'].append(match.group(1))
        result['year'] = match.group(2)
        return result

    match = re.search(f'^{person_name_expr},? {date_expr}$', value)
    if match:
        result['climbers'].append(match.group(1))
        # Assumin month/day/year format
        result['month'] = match.group(2)
        result['day'] = match.group(3)
        result['year'] = match.group(4)
        return result

    result['unknown_expression'] = True
    return result
