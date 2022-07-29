
from odoo import models, fields


class Task(models.Model):
    _inherit = "project.task"

    timebox_min_id = fields.Many2one('timebox', string='Timebox Min')
    timebox_max_id = fields.Many2one('timebox', string='Timebox Max')
