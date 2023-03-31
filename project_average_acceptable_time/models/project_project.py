
from odoo import models, fields, _, api


class Project(models.Model):
    _inherit = "project.project"

    average_acceptable_time = fields.Float('Average acceptable time')

    