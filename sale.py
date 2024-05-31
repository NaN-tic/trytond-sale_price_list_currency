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


class Line(metaclass=PoolMeta):
    __name__ = 'sale.line'

    @fields.depends('sale', '_parent_sale.price_list')
    def _get_context_sale_price(self):
        context = super()._get_context_sale_price()
        if self.sale:
            # sale_price_list module add price_list in the context
            # In case price_list has currency, set currency from the context to None
            # This will make that the core module will not try to convert the price
            # from the price list from company currency to price list currency.
            if getattr(self.sale, 'price_list', None):
                if self.sale.price_list.currency:
                    context['currency'] = None
        return context
