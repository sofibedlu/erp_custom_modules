{
    'name': 'Inventory Net Balance Report',
    'version': '15.0.1.0.0',
    'summary': 'Custom report to show inventory net balance',
    'description': """
        Custom report to show inventory net balance
    """,
    'category': 'Zergaw Customs/Inventory',
    'author': 'Zergaw',
    'website': 'https://zergaw.com',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/report_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}