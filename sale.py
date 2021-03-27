# This file is part sale_price_list_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @fields.depends('price_list', 'company', 'party')
    def on_change_with_currency(self, name=None):
        if self.price_list and self.price_list.currency:
            return self.price_list.currency.id
        elif self.company:
            return self.company.currency.id
