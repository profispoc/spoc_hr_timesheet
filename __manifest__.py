# -*- coding: utf-8 -*-
# Anton Berh    anton.berg.it@gmail.com
{
    'name': "SPOC HR Timesheet Extention",

    'summary': """Extends hr_timesheet module for S.P.O.C.""",

    'description': """
        For S.P.O.C intern project
    """,

    'author': "SPOC",
    'company': 'SPOC corp',
    'maintainer': 'SPOC corp',
    'website': "https://spoc-odoo.com.ua",
    'category': 'Productivity',
    'version': '16.0.1.0.0',

    'depends': ['base', 'hr_timesheet', 'sale_timesheet'],
    'sequence': 150,

    'license': "LGPL-3",
    'installable': True,
    'application': False,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/subtasks.xml',
        'wizards/project_reinit.xml',
        'wizards/subtasks_user.xml',
        'wizards/individual_task_recompute.xml',
        'views/views.xml',
    ],
}
