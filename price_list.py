# This file is part sale_price_list_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'
    currency = fields.Many2One('currency.currency', 'Currency',
        help="If a currency different from the company's is specified, "
            "the price will be based on the price list, and the exchange rate "
            "of the currency will not be applied.")
