def check_unique(data, field):
    values = set(item.get(field) for item in data if item.get(field))
    if not values:
        return True
    if len(values) != len(data):
        raise ValueError(f'Field "{field}" has to be unique')
    return True


def check_exactly_one(data, field):
    values = list(item.get(field) for item in data if item.get(field))
    if len(values) != 1:
        raise ValueError(f'It has to be exactly one item with active field "{field}"')
    return True
