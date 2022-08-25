from odoo import _, api, fields, models

class Users(models.Model):
    _inherit = "res.users"

    default_project_id = fields.Many2one('project.project', string='Default Project')