# -*- coding: utf-8 -*-
{
    'name': "Talabalar boshqaruvi",

    'summary': "Talabalar va guruhlarni boshqarish",

    'description': """
Talabalar va guruhlarni boshqarish
    """,

    'author': "Narzulla",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','course',],#'school_group','school_student','school_teacher','course',
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        # 'views/group_views.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': False,
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
}

