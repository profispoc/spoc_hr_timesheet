# -*- coding: utf-8 -*-
# Anton Berh    anton.berg.it@gmail.com
{
    'name': "SPOC HR Timesheet Extention",

    'summary': """Extends hr_timesheet module for S.P.O.C.""",

    'description': """
        For S.P.O.C intern project
    """,

    'author': "S.P.O.C.",
    'company': 'S.P.O.C. Business Automation Company',
    'maintainer': 'S.P.O.C. Business Automation Company',
    'website': "https://spoc-odoo.com.ua",
    'category': 'Productivity',
    'version': '2.0',

    'depends': ['base', 'hr_timesheet'],

    'license': "LGPL-3",
    'installable': True,
    'application': False,

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
