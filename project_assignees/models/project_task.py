
from odoo import models, fields, api


class Task(models.Model):
    _inherit = "project.task"

    assignee_ids = fields.Many2many('res.users', 'assignee_ids_rel', string='Assignees', tracking=True)

    @api.model
    def create(self, vals):
        '''
        assigned project manager to the task if nobody else is assigned to
        '''
        assignee_ids = vals.get('assignee_ids')
        project_id = vals.get('project_id')
        if project_id and self.env['project.project'].browse(project_id):
            project = self.env['project.project'].browse(project_id)
            if project.user_id:
                default_assignee_id = project.user_id.id
                if not assignee_ids or (assignee_ids and not assignee_ids[0][2]): #if assignee_ids doesnt existe or assignee_ids existe but is empty
                    vals['assignee_ids'] = [[6,0,[default_assignee_id]]]
        return super().create(vals)