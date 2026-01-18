{
    'name': "Product",

    'summary': "Product moduli",

    'description': """
Long description of module's purpose
    """,

    'author': "Narzulla",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/person_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/customer_views.xml',
        'views/employee_views.xml',
        'views/partner_views.xml',
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': False,
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}

