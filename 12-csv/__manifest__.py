# -*- coding: utf-8 -*-
{
    'name': "12-csv",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_setup'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_settings.views.xml',
        'data/ir_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
     #   'demo/demo.xml',
    ],
}
