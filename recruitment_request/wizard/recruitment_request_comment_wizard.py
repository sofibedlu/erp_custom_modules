from odoo import fields, models, api

class RecruitmentRequestCommentWizard(models.TransientModel):
    _name = 'recruitment.request.comment.wizard'
    _description = 'Recruitment Request Comment Wizard'

    comment = fields.Text('Comment', required=True)
    recruitment_request_id = fields.Many2one('recruitment.request', string='Recruitment Request')

    def action_submit_comment(self):
        context = dict(self._context or {})
        action = context.get('default_action')
        recruitment_request = self.recruitment_request_id
        if action == 'approve':
            recruitment_request.action_approve_by_ceo_with_comment(self.comment)
        elif action == 'reject':
            recruitment_request.action_reject_with_comment(self.comment)