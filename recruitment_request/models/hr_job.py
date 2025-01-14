from odoo import models, fields

class Job(models.Model):
    _inherit = 'hr.job'

    job_grade = fields.Char(string='Job Grade')