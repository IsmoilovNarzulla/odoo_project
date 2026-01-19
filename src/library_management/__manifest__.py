# -*- coding: utf-8 -*-
{
    'name': "library_management",

    'summary': "library_management",

    'description': """
Long description of module's purpose
    """,

    'author': "Narzulla",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/library_groups.xml',
        'security/ir.model.access.csv',
        'security/library_record_rules.xml',
        'views/views.xml',
        'views/library_menus.xml',
        'views/templates.xml',
        'views/library_rules.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'price': 0,
    'currency': 'USD',
}

