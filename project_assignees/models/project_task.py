
from odoo import models, fields


class Task(models.Model):
    _inherit = "project.task"

    assignee_ids = fields.Many2many('res.users', 'assignee_ids_rel', string='Assignees')

