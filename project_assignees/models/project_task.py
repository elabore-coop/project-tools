
from odoo import models, fields, _


class Task(models.Model):
    _inherit = "project.task"

    user_id = fields.Many2one(string="Owner")
    assignee_ids = fields.Many2many('res.users', 'assignee_ids_rel', string='Assignees')

