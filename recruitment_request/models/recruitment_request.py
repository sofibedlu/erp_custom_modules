from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import datetime


class RecruitmentRequest(models.Model):
    _name = 'recruitment.request'
    _description = 'Recruitment Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, copy=False, readonly=True, default='New')
    requester_id = fields.Many2one('res.users', string='Requested By', required=True, default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    job_position = fields.Many2one('hr.job', string='Job Position', required=True)
    job_title = fields.Char(string='Job Title')

    #new fields
    job_no = fields.Char(string='Job No')
    job_grade = fields.Char(string='Proposed Job Grade')
    employment_type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary')
    ], string='Type of Employment', default='full_time')
    education_level = fields.Selection([
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'Ph.D. or Doctorate'),
        ('other', 'Other'),
    ], string='Required Level of Education')
    field_of_study = fields.Char(help='Field of Study')
    professional_qualification = fields.Char(help='Desirable/Preferred Professional Qualification')
    experience_years = fields.Integer(string='Experience (Years)')
    work_place = fields.Char(string='Work Place')
    requested_date = fields.Date(string='Requested Date', required=True, default=fields.Date.context_today)
    justification = fields.Text(string='Justification for the Job')
    remarks = fields.Text(string='Remarks')
    ceo_comments = fields.Text(string='CEO Comments')

    number_of_employees = fields.Integer(string='Number of Employees', required=True, default=1)
    approval_comment = fields.Text('Approval Comment')
    rejection_comment = fields.Text('Rejection Comment')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('checked_by_hr_manager', 'Checked by HR Manager'),
        ('checked_by_hr_director', 'Checked by HR Director'),
        ('approved_by_chro', 'Approved by CHRO'),
        ('approved_by_ceo', 'Approved by CEO'),
        ('rejected', 'Rejected'),
        ('done', 'Done')
    ], string='Status', default='draft', tracking=True)

    @api.onchange('job_position')
    def _onchange_job_position(self):
        if self.job_position:
            self.job_grade = self.job_position.job_grade

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('recruitment.request') or 'New'
        return super(RecruitmentRequest, self).create(vals)
    
    def _validate_against_manpower_planning(self):
        """Validates the request against manpower planning with specific error messages."""
        current_year = datetime.now().year
        
        planning = self.env['manpower.planning'].search([
            ('job_position', '=', self.job_position.id),
            ('planning_year', '=', current_year),
            ('department_id', '=', self.department_id.id)
        ], limit=1)
        
        if not planning:
            raise ValidationError(
                "No manpower planning found for the selected job position, department and current year."
                )

        error_messages = []

        if planning.number_of_persons < self.number_of_employees:
            error_messages.append(
                f"The requested number of employees ({self.number_of_employees}) is above "
                f"the planned number of employees ({planning.number_of_persons})."
            )

        if error_messages:
            raise ValidationError(" ".join(error_messages))

    def action_submit(self):
        for request in self:
            request._validate_against_manpower_planning()
        self.state = 'submitted'
        gxmlid = 'recruitment_request.group_hr_manager'
        self._notify_responsible('submitted', gxmlid)

    def action_check_by_hr_manager(self):
        self.state = 'checked_by_hr_manager'
        self._notify_responsible('checked_by_hr_manager', 'recruitment_request.group_hr_director')

    def action_check_by_hr_director(self):
        self.state = 'checked_by_hr_director'
        self._notify_responsible('checked_by_hr_director', 'recruitment_request.group_chro')

    def action_approve_by_chro(self):
        self.state = 'approved_by_chro'
        self._notify_responsible('approved_by_chro', 'recruitment_request.group_ceo')

    def action_approve_by_ceo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Comment',
            'res_model': 'recruitment.request.comment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_action': 'approve',
                'default_recruitment_request_id': self.id
            }
        }

    def action_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Comment',
            'res_model': 'recruitment.request.comment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_action': 'reject',
                'default_recruitment_request_id': self.id
            }
        }
    
    def action_approve_by_ceo_with_comment(self, comment):
        self.state = 'approved_by_ceo'
        self.approval_comment = comment
        job_position = self.job_position
        if job_position:
            job_position.write({
                'department_id': self.department_id.id,
                'no_of_recruitment': self.number_of_employees,
                'description': self.remarks,
                'state': 'recruit'
            })
        template = self.env.ref('recruitment_request.mail_template_approved_by_ceo')
        self.message_post_with_template(
            template.id,
            partner_ids=[self.requester_id.partner_id.id],
            email_layout_xmlid='mail.mail_notification_light',
        )

    def action_reject_with_comment(self, comment):
        self.state = 'rejected'
        self.rejection_comment = comment
        template = self.env.ref('recruitment_request.mail_template_rejected')
        self.message_post_with_template(
            template.id,
            partner_ids=[self.requester_id.partner_id.id],
            email_layout_xmlid='mail.mail_notification_light',
        )

    def action_done(self):
        self.state = 'done'

    def _notify_responsible(self, state, group_xmlid):
        self.ensure_one()
        template = self.env.ref(f'recruitment_request.mail_template_{state}')
        if not template:
            return
        
        group = self.env.ref(group_xmlid, raise_if_not_found=False)
        if not group:
            return

        partner_ids = group.users.mapped('partner_id').ids

        if partner_ids:
            self.message_post_with_template(
                template.id,
                partner_ids=partner_ids,
                email_layout_xmlid='mail.mail_notification_light',
            )
