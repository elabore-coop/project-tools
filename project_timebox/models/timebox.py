from odoo import models, fields


class Task(models.Model):
    _name = "timebox"
    _description = "Timebox"

    name = fields.Char('name', required=True)
    sequence = fields.Integer()