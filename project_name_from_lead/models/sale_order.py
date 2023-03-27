from typing import ValuesView
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project_prepare_values(self):
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        if self.order_id and self.order_id.opportunity_id:
            values['name'] = self.order_id.opportunity_id.name        
        return values