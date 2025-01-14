{
    'name': 'Man Power Planning',
    'version': '1.0',
    'author': 'Sofi',
    'category': 'Zergaw Customs/HR',
    'summary': 'Man Power Planning module for recruitment',
    'description': """
        This module allows you to plan your manpower requirements.
    """,
    'author': 'sofi',
    'depends': ['recruitment_request'],
    'data': [
        'security/manpower_planning_security.xml',
        'security/ir.model.access.csv',
        'views/manpower_planning_views.xml',
    ],
    'installable': True,
    'application': False,
}