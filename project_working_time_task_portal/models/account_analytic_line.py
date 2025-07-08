# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models
from odoo.osv import expression


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _timesheet_get_portal_domain(self):
        domain = super()._timesheet_get_portal_domain()
        return expression.AND([domain, [("exclude_from_sale_order", "=", False)]])
