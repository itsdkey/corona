from collections import OrderedDict
from decimal import ROUND_HALF_UP, Decimal


def calculate_growth_factor(data: OrderedDict) -> OrderedDict:
    """Calculate the growth factor.

    :param data: data to use
    """
    first_key = '2020-03-04'
    previous_cases = data.get(first_key)['cases']
    for key, value in data.items():
        growth_factor = Decimal(
            value['cases'] / previous_cases,
        ).quantize(Decimal('0.000'), ROUND_HALF_UP)

        value['growth_factor'] = growth_factor
        previous_cases = value['cases']

    return data
