
from odoo import models, fields, _, api


class Task(models.Model):
    _inherit = "project.task"

    assignee_ids = fields.Many2many('res.users', 'assignee_ids_rel', string='Other Assignees')

    @api.multi
    def subscribe_assignees(self):
        for task in self:
            partner_ids = [a.partner_id.id for a in task.assignee_ids]
            task.message_subscribe(partner_ids)

    @api.multi
    def write(self, vals):
        result = super(Task, self).write(vals)
        self.subscribe_assignees()
        return result
    
    @api.model
    def create(self, vals):
        task = super(Task, self).create(vals)
        task.subscribe_assignees()
        return task