from odoo import models

class Lead(models.Model):
    _inherit = 'crm.lead'

    def write(self, vals):
        """update project name if project created from lead        
        """
        for lead in self:
            if 'name' in vals:
                sale = self.env['sale.order'].search([('opportunity_id','=',lead.id)])
                if sale:
                    project = self.env['project.project'].search([('sale_order_id','=',sale.id)])
                    if project:
                        project.name = vals['name']

        return super(Lead, self).write(vals)
