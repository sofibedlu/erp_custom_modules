from odoo import models, fields

class AssessmentForm(models.Model):
    _name = 'assessment.form'
    _description = 'Assessment Form Template'

    name = fields.Char(string='Form Name', required=True)
    line_ids = fields.One2many('assessment.form.line', 'form_id', string='Questions')

class AssessmentFormLine(models.Model):
    _name = 'assessment.form.line'
    _description = 'Assessment Form Question'

    form_id = fields.Many2one('assessment.form', string='Assessment Form', ondelete='cascade', required=True)
    question_number = fields.Integer(string='#')
    question = fields.Text(string='Question', required=True)