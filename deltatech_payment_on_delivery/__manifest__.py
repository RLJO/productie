# ©  2015-2020 Deltatech
# See README.rst file on addons root folder for license details
{
    "name": "Cash On Delivery",
    "summary": "Cash On Delivery",
    "version": "14.0.4.0.3",
    "author": "Terrabit, Dorin Hongu",
    "website": "https://www.terrabit.ro",
    "support": "odoo@terrabit.ro",
    "category": "Accounting",
    "depends": ["payment", "website_sale", "deltatech_website_delivery_and_payment"],
    "external_dependencies": {
        "python": ["xlrd"],
    },
    "data": [
        "views/payment_templates.xml",
        "data/payment_acquirer_data.xml",
        # "views/transaction_view.xml",
        "views/assets.xml",
        "views/payment_view.xml",
        "security/ir.model.access.csv",
        "wizard/payment_import_view.xml",
    ],
    "qweb": ["static/src/xml/transaction_lines.xml"],
    "price": 50.00,
    "currency": "EUR",
    "license": "LGPL-3",
    "images": ["static/description/main_screenshot.png"],
    "development_status": "Production/Stable",
    "uninstall_hook": "uninstall_hook",
    "maintainers": ["dhongu"],
}
