# -*- coding: utf-8 -*-

from odoo import _, fields, models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    funding_wish = fields.Selection([("free", "Free"),("accepted", "Payment accepted"),("expected", "Payment expected")], string=_("Funding wish"), copy=False)
    treated = fields.Boolean(string=_("Treated"), copy=False)
    
    