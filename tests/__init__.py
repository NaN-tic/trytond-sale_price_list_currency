# This file is part sale_price_list_currency module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.sale_price_list_currency.tests.test_sale_price_list_currency import suite
except ImportError:
    from .test_sale_price_list_currency import suite

__all__ = ['suite']
