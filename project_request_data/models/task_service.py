from odoo import models, fields


class TaskService(models.Model):
    _name = "task.service"
    _description = "Task service"

    name = fields.Char('name', required=True)
    sequence = fields.Integer()