from odoo import models, fields, api


class Task(models.Model):
    _inherit = 'project.task'

    first_assignee_id = fields.Many2one('res.users', string='First Assignee', compute='_compute_first_assignee')

    @api.depends('assignee_ids')
    def _compute_first_assignee(self):
        for record in self:
            record.first_assignee_id = record.assignee_ids[:1].id if record.assignee_ids else False

