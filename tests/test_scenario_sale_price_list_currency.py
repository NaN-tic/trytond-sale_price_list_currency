import datetime
import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import create_chart, create_fiscalyear
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.modules.currency.tests.tools import get_currency
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        today = datetime.date.today()

        # Install sale_price_list
        activate_modules('sale_price_list_currency')

        # Create company
        _ = create_company()
        company = get_company()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)

        # Create parties
        Party = Model.get('party.party')
        customer = Party(name='Customer')
        customer.save()
        customer_without_price_list = Party(name='Customer without price list')
        customer_without_price_list.save()
        customer2 = Party(name='Customer2')
        customer2.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.salable = True
        template.list_price = Decimal('10')
        template.save()
        product, = template.products
        template = ProductTemplate()
        template.name = 'service'
        template.default_uom = unit
        template.type = 'service'
        template.salable = True
        template.list_price = Decimal('30')
        template.save()

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create currencies
        euro = get_currency(code='EUR')
        usd = get_currency(code='USD')

        # Create currency rate
        CurrencyRate = Model.get('currency.currency.rate')
        currency_rate = CurrencyRate()
        currency_rate.date = today
        currency_rate.rate = Decimal(1.5)
        currency_rate.currency = euro  # company has usd currency
        currency_rate.save()

        # Create a price List and assign it to customer
        PriceList = Model.get('product.price_list')
        price_list = PriceList(name='Retail')
        price_list.currency = euro
        price_list_line = price_list.lines.new()
        price_list_line.formula = '10.0'
        price_list.save()
        customer.sale_price_list = price_list
        customer.save()

        # Create a price List and assign it to customer2
        price_list2 = PriceList(name='Retail 2')
        price_list2.currency = usd
        price_list_line2 = price_list2.lines.new()
        price_list_line2.formula = '8.5'
        price_list2.save()
        customer2.sale_price_list = price_list2
        customer2.save()

        # Create a sale and customer
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = customer
        self.assertEqual(sale.price_list, price_list)
        self.assertEqual(sale.currency, euro)

        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        sale_line.quantity = 1.0
        self.assertEqual(sale_line.unit_price, Decimal('10.0000'))
        sale.save()

        # Create a sale and customer2
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = customer2
        self.assertEqual(sale.price_list, price_list2)
        self.assertEqual(sale.currency, usd)

        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        sale_line.quantity = 1.0
        self.assertEqual(sale_line.unit_price, Decimal('8.5000'))
        sale.save()

        # Create a sales without price list and apply currency rate
        sale = Sale()
        sale.party = customer
        sale.price_list = None
        sale.currency = euro
        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        sale_line.quantity = 1.0
        self.assertEqual(sale_line.unit_price, Decimal('15.0000'))

        sale = Sale()
        sale.party = customer2
        sale.price_list = None
        sale.currency = usd
        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        sale_line.quantity = 1.0
        self.assertEqual(sale_line.unit_price, Decimal('10.0000'))

        # Create a sales with price list currency diferent sale currency and company currency
        sale = Sale()
        sale.party = customer
        self.assertEqual(sale.price_list, price_list)
        self.assertEqual(sale.currency, euro)

        sale.currency = usd
        self.assertNotEqual(sale.price_list.currency, sale.currency)

        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        sale_line.quantity = 1.0
        self.assertEqual(sale_line.unit_price, Decimal('6.6667'))
