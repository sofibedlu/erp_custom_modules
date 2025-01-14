from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class ManPowerPlanning(models.Model):
    _name = 'manpower.planning'
    _description = 'Man Power Planning Record'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    job_position = fields.Many2one('hr.job', string='Job Position', required=True)
    job_number = fields.Char(string='Job Number')
    job_grade = fields.Char(string='Job Grade')
    number_of_persons = fields.Integer(string='# of Persons', required=True)
    type_of_employment = fields.Selection([
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship')
    ], string='Type of Employment')
    person_specifications = fields.Text(help='Person Specifications/Qualifications')
    level_of_education = fields.Selection([
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'Ph.D. or Doctorate'),
        ('other', 'Other'),
    ], string='Level of Education')
    field_of_study = fields.Char(help='Field of Study/Professional Qualification or Specialization or Certification')
    desirable_qualification = fields.Char(help='Desirable/Preferred Professional Qualification')
    experience_years = fields.Integer(string='Experience (Year)')
    skill_set = fields.Char(help='Skill Set or Additional Personnel Qualities')
    english_competency = fields.Selection([
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('fluent', 'Fluent')
    ], string='English Language Competency')
    remarks = fields.Text(string='Remarks')

    planning_year = fields.Integer(string="Planning Year", required=True, default=lambda self: datetime.now().year)

    @api.depends('department_id', 'job_position')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.department_id.name} - {record.job_position.name}" if record.department_id and record.job_position else "Manpower Planning"
            
    @api.onchange('job_position')
    def _onchange_job_position(self):
        if self.job_position:
            self.job_grade = self.job_position.job_grade

    @api.constrains('planning_year')
    def _check_planning_year(self):
        """Ensures that the planning year is greater than or equal to the current year."""
        for record in self:
          current_year = datetime.now().year
          if record.planning_year < current_year:
              raise ValidationError(
                  "The Planning Year must be greater than or equal to the current year."
              )