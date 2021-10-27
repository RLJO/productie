# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details
{
    "name": "Banca Transilvania iPay Payment Acquirer",
    "summary": "BT iPay Payment Acquirer",
    "version": "14.0.0.0.2",
    "author": "Terrabit, Dorin Hongu",
    "website": "https://www.terrabit.ro",
    "support": "odoo@terrabit.ro",
    "category": "Accounting",
    "depends": ["payment", "website_sale", "phone_validation"],
    "external_dependencies": {"python": ["phonenumbers"]},
    "data": ["views/payment_templates.xml", "views/payment_views.xml", "data/payment_acquirer_data.xml"],
    "price": 200.00,
    "currency": "EUR",
    "license": "LGPL-3",
    "images": ["static/description/main_screenshot.png"],
    "development_status": "Mature",
    "maintainers": ["dhongu"],
}
