{
    'name': "openacademy",
    'summary': """
        This module was created to manage an academy.""",
    'author': "Vauxoo",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    "license": "LGPL-3",
    'version': '13.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'board'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/openacademy_course_view.xml',
        'views/openacademy_partner_view.xml',
        'wizard/openacademy_wizard_view.xml',
        'views/openacademy_session_board_view.xml',
        'reports/openacademy_session_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/openacademy_course_demo.xml',
    ],
}
