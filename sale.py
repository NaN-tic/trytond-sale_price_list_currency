# This file is part sale_price_list_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.modules.product import round_price


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
            if getattr(self.sale, 'price_list', None):
                if self.sale.price_list.currency:
                    context['currency'] = None
        return context

    @fields.depends('sale', 'currency')
    def compute_unit_price(self):
        pool = Pool()
        Date = pool.get('ir.date')
        Currency = pool.get('currency.currency')

        today = Date.today()

        unit_price = super().compute_unit_price()

        currency_price_list = self.sale and self.sale.price_list and self.sale.price_list.currency
        currency_sale = self.currency

        if currency_price_list and (currency_price_list != currency_sale):
            date = Transaction().context.get('sale_date') or today
            with Transaction().set_context(date=date):
                new_unit_price = Currency.compute(
                    currency_price_list, unit_price,
                    currency_sale, round=False)
                if new_unit_price is not None:
                    unit_price = round_price(new_unit_price)
        return unit_price
