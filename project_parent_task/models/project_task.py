
from odoo import models, fields, api

class Task(models.Model):
    _inherit = "project.task"

    #overwrite others def _compute_sale_line(self)
    #we want to skip _compute_sale_line in /home/laetitia/elabore/odoo/OCB/addons/sale_timesheet/models/project.py file
    
    @api.depends('commercial_partner_id', 'sale_line_id.order_partner_id.commercial_partner_id', 'parent_id.sale_line_id', 'project_id.sale_line_id')
    def _compute_sale_line(self):
        for task in self:
            # check sale_line_id and customer are coherent
            if task.sale_line_id.order_partner_id.commercial_partner_id != task.partner_id.commercial_partner_id:
                task.sale_line_id = False
            if not task.sale_line_id:
                task.sale_line_id = task.parent_id.sale_line_id or task.project_id.sale_line_id

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        self.sale_line_id = self.parent_id.sale_line_id or self.project_id.sale_line_id