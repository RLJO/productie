# -*- coding: utf-8 -*-

{
    'name': 'Push Post to Website Visitors',
    'author': 'I.L. Muntean',
    'version': '1.0',
    'category': 'Base',
    'sequence': 20,
    'summary': 'Push Post to Website Visitors',
    'description': """
Push Post to Website Visitors
=============================

Push Post to Website Visitors

    """,
    'website': 'https://www.information-systems.ro',
    'depends': ['social_push_notifications'],
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/social_push_wizard.xml',
    ],
    'demo': [
    ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
