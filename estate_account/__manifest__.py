# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate Account',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 25,
    'summary': 'Offer and sell real estate',
    'depends': [
        'base_setup',
        'estate',
        'account',
    ],
    'data': [
        'views/estate_properties_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
