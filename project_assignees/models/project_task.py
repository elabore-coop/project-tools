
from odoo import models, fields, api


class Task(models.Model):
    _inherit = "project.task"

    assignee_ids = fields.Many2many('res.users', 'assignee_ids_rel', string='Assignees', tracking=True)

    @api.model
    def create(self, vals):
        '''
        assigned project manager to the task if nobody else is assigned to
        '''
        assignee_ids = vals.get('assignee_ids', [])
        project_id = vals.get('project_id', [])
        if project_id and assignee_ids and not assignee_ids[0][2]:
            project = self.env['project.project'].browse(project_id)
            if project and project.user_id: assignee_ids[0][2] = str(project.user_id.id)
        return super().create(vals)