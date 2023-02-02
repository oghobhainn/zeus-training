{
    'name': 'Real Estate',
    'version': '1.0',
    'depends': ['base',
                'base_setup',
                ],
    'author': 'Marjan Vanhixe',
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto-install': False
}