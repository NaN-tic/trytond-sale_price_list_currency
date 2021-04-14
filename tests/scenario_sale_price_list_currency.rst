=================================
Sale Price List Currency Scenario
=================================

Imports::

    >>> import datetime
    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules, set_user
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts
    >>> from trytond.modules.currency.tests.tools import get_currency
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term

Install sale_price_list::

    >>> config = activate_modules('sale_price_list_currency')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()
    >>> customer_without_price_list = Party(name='Customer without price list')
    >>> customer_without_price_list.save()
    >>> customer2 = Party(name='Customer2')
    >>> customer2.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')

    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.save()
    >>> product, = template.products

    >>> template = ProductTemplate()
    >>> template.name = 'service'
    >>> template.default_uom = unit
    >>> template.type = 'service'
    >>> template.salable = True
    >>> template.list_price = Decimal('30')
    >>> template.save()
    >>> service, = template.products

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create currencies::

    >>> euro = get_currency(code='EUR')
    >>> usd = get_currency(code='USD')

Create a price List and assign it to customer::

    >>> PriceList = Model.get('product.price_list')
    >>> price_list = PriceList(name='Retail')
    >>> price_list.currency = euro
    >>> price_list_line = price_list.lines.new()
    >>> price_list_line.formula = '10.0'
    >>> price_list.save()
    >>> customer.sale_price_list = price_list
    >>> customer.save()

Create a price List and assign it to customer2::

    >>> price_list2 = PriceList(name='Retail 2')
    >>> price_list2.currency = usd
    >>> price_list_line2 = price_list2.lines.new()
    >>> price_list_line2.formula = '8.5'
    >>> price_list2.save()
    >>> customer2.sale_price_list = price_list2
    >>> customer2.save()

Create a sale and customer::

    >>> Sale = Model.get('sale.sale')
    >>> sale = Sale()
    >>> sale.party = customer
    >>> sale.price_list == price_list
    True
    >>> sale.currency == euro
    True
    >>> sale.payment_term = payment_term
    >>> sale_line = sale.lines.new()
    >>> sale_line.product = product
    >>> sale_line.quantity = 1.0
    >>> sale_line.unit_price
    Decimal('20.0000')
    >>> sale.save()

Create a sale and customer2::

    >>> Sale = Model.get('sale.sale')
    >>> sale = Sale()
    >>> sale.party = customer2
    >>> sale.price_list == price_list2
    True
    >>> sale.currency == usd
    True
    >>> sale.payment_term = payment_term
    >>> sale_line = sale.lines.new()
    >>> sale_line.product = product
    >>> sale_line.quantity = 1.0
    >>> sale_line.unit_price
    Decimal('8.5000')
    >>> sale.save()
