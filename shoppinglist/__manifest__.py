{
    'name': 'Shopping List',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Marjan Vanhixe',
    'data': [
        'security/ir.model.access.csv',

        'views/status_list.xml',
        'views/shopping_list_detail_view.xml',
        'views/shopping_list_view.xml',
        'views/shopping_list_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto-install': False
}