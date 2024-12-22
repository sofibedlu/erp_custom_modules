from odoo import models, fields
from odoo.exceptions import ValidationError

class Applicant(models.Model):
    _inherit = 'hr.applicant'


    assessment_form_id = fields.Many2one('assessment.form', string='Assessment Form')
    assessment_ids = fields.One2many("applicant.assessment", 'applicant_id', string="Applicant Assessments")
    assessment_count = fields.Integer(string="Assessment Count", compute="_compute_assessment_count")

    def _compute_assessment_count(self):
        for rec in self:
           rec.assessment_count = len(rec.assessment_ids)

    def write(self, vals):
        res = super(Applicant, self).write(vals)
        if "assessment_form_id" in vals:
            for rec in self:
                existing_assessment = self.env["applicant.assessment"].search([
                    ('form_id', '=', rec.assessment_form_id.id),
                    ('applicant_id', '=', rec.id)
                ])
                if not existing_assessment:
                    vals_list = [{"form_id": rec.assessment_form_id.id, "applicant_id": rec.id}]
                    assessment_id = self.env["applicant.assessment"].create(vals_list)
                    for line in rec.assessment_form_id.line_ids:
                        self.env['applicant.assessment.line'].create({"form_line_id": line.id, "assessment_id": assessment_id.id})
        return res