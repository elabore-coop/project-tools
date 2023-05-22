
from odoo import models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    privacy_visibility = fields.Selection(
        selection_add=[('followers_portal','Invited portal users and invited internal users')], 
        ondelete={'followers_portal': 'set default'})

    @api.model
    def create(self, vals):
        """In case of "followers_portal" privacy visibility, add current user to list of allowed users.
        Same behaviour than "portal" privacy visibility.
        """
        project = super(Project, self).create(vals)        
        if project.privacy_visibility == 'followers_portal' and project.partner_id.user_ids:
            project.allowed_user_ids |= project.partner_id.user_ids
        return project
    
    def write(self, vals):
        """In case of "followers_portal" privacy visibility, add current user to list of allowed users.
        Same behaviour than "portal" privacy visibility.
        """
        res = super(Project, self).write(vals)
        if vals.get('partner_id') or vals.get('privacy_visibility'):
            for project in self.filtered(lambda project: project.privacy_visibility == 'followers_portal'):
                project.allowed_user_ids |= project.partner_id.user_ids
        return res