
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    project_ids = fields.Many2many('project.project', name="Projects", compute='get_related_project_ids')
    project_count = fields.Integer("Project Count", compute='get_related_project_ids')
    projects_name = fields.Char('Project(s)', compute='get_related_project_ids')

    def action_open_projects(self):
        '''
            Open related projects, in form or tree view depending on project numbers
        '''
        project_ids = self.project_ids.ids
        action = self.env["ir.actions.actions"]._for_xml_id("project.open_view_project_all")

        if self.project_count == 1:
            action['res_id'] = project_ids[0]
            action['views'] = [[False, "form"]]
        else:
            action['views'] = [[False, "tree"], [False, "form"]]
        
        action['domain'] = [('id', 'in', project_ids)]

        del action['target'] #to display breadcrumbs
        
        return action


    @api.depends('line_ids.sale_line_ids')
    def get_related_project_ids(self):
        for move in self:
            projects = self.env['project.task'].search([('sale_order_id','in',move.line_ids.sale_line_ids.order_id.ids)]).project_id
            move.project_ids = projects.ids
            move.projects_name = ' ; '.join([p.name for p in projects])
            move.project_count = len(projects)