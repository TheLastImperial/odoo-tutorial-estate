{
    'name': "Estate",
    'description': """
        Tutorial app. To administrate houses.
    """,
    'author': "TheLastImperial",
    'website': 'https://github.com/TheLastImperial/odoo-tutorial-estate',
    'category': 'Tutorials',
    'version': '0.0.6',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menu_views.xml',
    ],
}
