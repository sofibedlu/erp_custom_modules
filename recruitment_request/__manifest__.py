{
    'name': 'Recruitment Request',
    'version': '1.0',
    'category': 'Zergaw Customs/HR',
    'summary': 'Module for requesting recruitment',
    'description': 'Module for requesting recruitment and managing approvals.',
    'author': 'Sofi',
    'depends': ['base', 'hr', 'mail', 'web', 'hr_recruitment'],
    'data': [
        'security/recruitment_request_security.xml',
        'security/ir.model.access.csv',
        'views/recruitment_request_views.xml',
        'views/hr_job_views.xml',
        'views/recruitment_request_comment_wizard_view.xml',
        'data/mail_templates.xml',
        'data/seq.xml',
        
    ],
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_backend': [
            'recruitment_request/static/src/js/priority_tag.js',
            'recruitment_request/static/src/css/priority_tag.css',
        ],
    }
}