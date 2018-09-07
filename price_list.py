# This file is part sale_price_list_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction

__all__ = ['PriceList']


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'
    currency = fields.Many2One('currency.currency', 'Currency')

    @classmethod
    def default_currency(cls):
        Company = Pool().get('company.company')

        company_id = Transaction().context.get('company')
        if company_id:
            company = Company(company_id)
            return company.currency.id
