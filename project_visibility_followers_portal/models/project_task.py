
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = "project.task"

    @api.constrains('message_partner_ids')
    def _check_no_portal_allowed(self):
        for task in self.filtered(lambda t: t.project_id.privacy_visibility not in ('portal','followers_portal')):
            portal_users = task.message_partner_ids.user_ids.filtered('share')
            if portal_users:
                user_names = ', '.join(portal_users[:10].mapped('name'))
                raise ValidationError(_("The project visibility setting doesn't allow portal users to see the project's tasks. (%s)", user_names))

    def _compute_access_warning(self):        
        for task in self.filtered(lambda x: x.project_id.privacy_visibility not in ('portal','followers_portal')):
            task.access_warning = _(
                "The task cannot be shared with the recipient(s) because the privacy of the project is too restricted. Set the privacy of the project to 'Visible by following customers' in order to make it accessible by the recipient(s).")
            

    
    @api.model_create_multi
    def create(self, vals_list):
        tasks = super(Task, self).create(vals_list)
        for task in tasks:
            if task.project_id.privacy_visibility == 'followers_portal':
                task._portal_ensure_token()
        return tasks
    
    def _notify_get_groups(self, msg_vals=None):
        groups = super(Task, self)._notify_get_groups(msg_vals=msg_vals)
        """ Handle project users and managers recipients that can assign
        tasks and create new one directly from notification emails. Also give
        access button to portal users and portal customers. If they are notified
        they should probably have access to the document. """
        self.ensure_one()

        project_user_group_id = self.env.ref('project.group_project_user').id
        project_manager_group_id = self.env.ref('project.group_project_manager').id

        group_func = lambda pdata: pdata['type'] == 'user' and project_user_group_id in pdata['groups']
        if self.project_id.privacy_visibility == 'followers_portal':
            message_partner_ids = self.project_id.message_partner_ids.partner_id.ids
            group_func = lambda pdata:\
                pdata['type'] == 'user'\
                and (
                        project_manager_group_id in pdata['groups']\
                        or (project_user_group_id in pdata['groups'] and pdata['id'] in message_partner_ids)
                )
            groups = [('group_project_user', group_func, {})]+groups
            message_partner_ids = self.project_id.message_partner_ids
            groups.insert(0, (
                'message_partner_ids',
                lambda pdata: pdata['type'] == 'portal' and pdata['id'] in message_partner_ids,
                {}
            ))

        return groups