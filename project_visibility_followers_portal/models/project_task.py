
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = "project.task"

    @api.constrains('allowed_user_ids')
    def _check_no_portal_allowed(self):
        for task in self.filtered(lambda t: t.project_id.privacy_visibility not in ('portal','followers_portal')):
            portal_users = task.allowed_user_ids.filtered('share')
            if portal_users:
                user_names = ', '.join(portal_users[:10].mapped('name'))
                raise ValidationError(_("The project visibility setting doesn't allow portal users to see the project's tasks. (%s)", user_names))
            
    @api.depends('project_id.allowed_user_ids', 'project_id.privacy_visibility')
    def _compute_allowed_user_ids(self):
        for task in self.with_context(prefetch_fields=False):
            portal_users = task.allowed_user_ids.filtered('share')
            internal_users = task.allowed_user_ids - portal_users

            if task.project_id.privacy_visibility == 'followers':
                task.allowed_user_ids |= task.project_id.allowed_internal_user_ids
                task.allowed_user_ids -= portal_users
            elif task.project_id.privacy_visibility == 'portal':
                task.allowed_user_ids |= task.project_id.allowed_portal_user_ids
            elif task.project_id.privacy_visibility == 'followers_portal':
                task.allowed_user_ids |= task.project_id.allowed_internal_user_ids
                task.allowed_user_ids |= task.project_id.allowed_portal_user_ids

            if task.project_id.privacy_visibility not in ('portal','followers_portal'):
                task.allowed_user_ids -= portal_users
            elif task.project_id.privacy_visibility not in ('followers','followers_portal'):
                task.allowed_user_ids -= internal_users

    def _compute_access_warning(self):        
        for task in self.filtered(lambda x: x.project_id.privacy_visibility not in ('portal','followers_portal')):
            task.access_warning = _(
                "The task cannot be shared with the recipient(s) because the privacy of the project is too restricted. Set the privacy of the project to 'Visible by following customers' in order to make it accessible by the recipient(s).")
            
    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        """
        Add the users subscribed to allowed portal users
        """
        res = super(Task, self).message_subscribe(partner_ids=partner_ids, channel_ids=channel_ids, subtype_ids=subtype_ids)
        if partner_ids:
            new_allowed_users = self.env['res.partner'].browse(partner_ids).user_ids.filtered('share')
            tasks = self.filtered(lambda task: task.project_id.privacy_visibility == 'followers_portal')
            tasks.sudo().allowed_user_ids |= new_allowed_users
        return res
    
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
            allowed_user_ids = self.project_id.allowed_internal_user_ids.partner_id.ids
            group_func = lambda pdata:\
                pdata['type'] == 'user'\
                and (
                        project_manager_group_id in pdata['groups']\
                        or (project_user_group_id in pdata['groups'] and pdata['id'] in allowed_user_ids)
                )
            groups = [('group_project_user', group_func, {})]+groups
            allowed_user_ids = self.project_id.allowed_portal_user_ids.partner_id.ids
            groups.insert(0, (
                'allowed_portal_users',
                lambda pdata: pdata['type'] == 'portal' and pdata['id'] in allowed_user_ids,
                {}
            ))

        return groups