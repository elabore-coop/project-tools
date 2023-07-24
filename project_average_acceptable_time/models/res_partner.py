
from odoo import models, fields, _, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    average_acceptable_time = fields.Float('Average acceptable time') # not used, but necessary to post custom field from /my/account

    