# This file is part sale_price_list_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import price_list
from . import sale

def register():
    Pool.register(
        price_list.PriceList,
        sale.Sale,
        module='sale_price_list_currency', type_='model')
