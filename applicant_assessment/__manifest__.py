{
    'name': 'Applicant Assessment',
    'author': 'sofi',
    'version': '1.0',
    'summary': 'Manage and record assessments for job applicants.',
    'description': 'Allows selecting and filling out different assessment forms for applicants.',
    'category': 'Human Resources',
    'depends': ['hr_recruitment'],
    'data': [
        'security/applicant_assessments.xml',
        'security/ir.model.access.csv',
        'views/assessment_form_views.xml',
        'views/applicant_assessment_views.xml',
        'views/applicant_views.xml',

    ],
    'installable': True,
    'auto_install': False,
}