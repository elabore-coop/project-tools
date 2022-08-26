
from odoo import models, fields


class Task(models.Model):
    _inherit = "project.task"

    service_id = fields.Many2one('task.service', string='Service')
    request_type_id = fields.Many2one('request.type', string='Request Type')
