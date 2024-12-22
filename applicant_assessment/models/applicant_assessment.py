from odoo import models, fields, api
from datetime import date

class ApplicantAssessment(models.Model):
    _name = 'applicant.assessment'
    _description = 'Applicant Assessment Data'

    applicant_id = fields.Many2one('hr.applicant', string='Applicant', required=True, ondelete='cascade')
    partner_name = fields.Char(related='applicant_id.partner_name', string='Applicant Name', store=True, readonly=True)
    form_id = fields.Many2one('assessment.form', string='Assessment Form', required=True)
    line_ids = fields.One2many('applicant.assessment.line', 'assessment_id', string='Answers')
    total_score = fields.Integer(string='Total Score', compute='_compute_total_score', store=True)
    notes = fields.Text(string='Notes/Comments')
    interviewer_name = fields.Char(string='Interviewer')
    interviewer_signature = fields.Binary(string='Signature')
    interview_date = fields.Date(string='Date', default=lambda self: date.today())
    current_earning = fields.Float(string='Current Earning')
    expected_salary = fields.Float(string='Expected Salary')
    expected_start_date = fields.Date(string='Expected Starting Date')
    expected_benefits = fields.Text(string='Expected Additional Benefits')

    job_id = fields.Many2one('hr.job', string='Position', related='applicant_id.job_id', readonly=True)
    education = fields.Char(string='Education')
    relevant_work_experience = fields.Text(string='Relevant Work Experience')
    recommendation = fields.Selection([
        ('hire_now', 'Hire Now'),
        ('do_not_hire', 'Do Not Hire'),
        ('indifferent', 'Indifferent')
    ], string='Recommendation')
      
    @api.depends('line_ids.score')
    def _compute_total_score(self):
        for rec in self:
            total_score = 0
            for line in rec.line_ids:
                
                if line.score:
                    total_score += line.score
            rec.total_score = total_score


class ApplicantAssessmentLine(models.Model):
    _name = 'applicant.assessment.line'
    _description = 'Applicant Assessment Answer'

    assessment_id = fields.Many2one('applicant.assessment', string='Assessment', ondelete='cascade', required=True)
    question_number = fields.Integer(string='#', related='form_line_id.question_number', readonly=True)
    question = fields.Text(string='Question', related='form_line_id.question', readonly=True)
    form_line_id = fields.Many2one('assessment.form.line', string="Question Form Line")
    score = fields.Integer(string='Score')