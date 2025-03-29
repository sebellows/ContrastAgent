from app.agent.configuration import locales


def get_attributes(instance):
    if not isinstance(instance, object):
        raise ValueError('Argument for get_attributes must be a class instance')
    class_items = instance.__class__.__dict__.items()
    return { k: v for k, v in class_items if not k.startswith('_') and not isinstance(v, property) }

def get_properties(instance):
    if not isinstance(instance, object):
        raise ValueError('Argument for get_properties must be a class instance')
    class_items = instance.__class__.__dict__.items()
    return { k: getattr(instance, k) for k, v in class_items if isinstance(v, property) }

def get_all_properties(instance):
    if not isinstance(instance, object):
        raise ValueError('Argument for get_all_properties must be a class instance')
    return { **get_attributes(instance), **get_properties(instance) }


DEFAULT_AMOUNT = '000'

def format_price(
    locale: str,
    value: int | str = DEFAULT_AMOUNT,
    use_symbol = False
):
    loc = locales.get(locale[3:])
    separator = loc.get('decimal_separator', None)
    decimals = loc.get('currency_decimal_spaces', 0)
    amount = str(value)
    if decimals > 0 and separator:
        # Right-pad the amount value if length less than or equal to
        # the number of decimal spaces when formatting currency.
        if separator in amount:
            bills, cents = amount.split(separator)
            if int(cents) < decimals:
                rem = decimals - int(cents)
                amount = bills + cents
                amount += DEFAULT_AMOUNT[:-len(rem)]
        elif len(amount) <= decimals:
            amount += DEFAULT_AMOUNT[:-len(decimals)]
    price = amount
    if decimals > 0:
        bills = amount[0:-decimals]
        price = bills + separator + amount[len(bills):]

    if use_symbol:
        sym = loc.get('currency_symbol', '$')
        pos = loc.get('symbol_position', 'start')
        price = price + sym if pos == 'end' else sym + price

    return price
