# -*- coding: utf-8 -*-
###############################################################################
# Author : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
###############################################################################

{
    'name': 'Mail Template Multi Company',
    'version': '1.0',
    'summary': 'This module is used to manage multi-company mail templates and send different emails from different companies across all the models in odoo.',
    'description': """Mail Template Multi Company send mail from multi Company if selected true in mail template.
    """,
    'category': 'Tools',
    'author': 'Kanak Infosystems LLP.',
    'website': 'http://www.kanakinfosystems.com',
    'depends': ['sale_management', 'mail'],
    'data': [
        'views/knk_mail_template_view.xml'
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
    'price': 35,
    'currency': 'EUR',
    'live_test_url': 'https://kanakinfosystems.com/contactus',
}
