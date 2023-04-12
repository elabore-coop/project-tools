
from odoo import models, fields, _, api

        


class MailTracking(models.Model):
    _inherit = 'mail.tracking.value'

    @api.model
    def create_tracking_values(self, initial_value, new_value, col_name, col_info, track_sequence):
        """
        Track values of assignees changes in chatter
        """
        if col_name == 'assignee_ids' and initial_value:
            values = {'field': col_name, 'field_desc': col_info['string'], 'field_type': col_info['type'], 'track_sequence': track_sequence}
            values.update({
                'old_value_char': ', '.join([i.name for i in initial_value]),
                'new_value_char': ', '.join([i.name for i in new_value])
            })
            return values
        return super(MailTracking, self).create_tracking_values(initial_value, new_value, col_name, col_info, track_sequence)

class Task(models.Model):
    _inherit = "project.task"

    assignee_ids = fields.Many2many('res.users', 'assignee_ids_rel', string='Other Assignees', track_visibility='change')

    @api.multi
    def subscribe_and_notify_assignees(self, new_assignee_ids=None):
        for task in self:
            # Use assignees on parameter if exists
            if new_assignee_ids:
                assignees = self.env['res.users'].browse(new_assignee_ids)
            else:
                assignees = task.assignee_ids

            # Subscribe partners
            partner_ids = [a.partner_id.id for a in assignees]            
            task.message_subscribe(partner_ids)
            
            # Send notification to assignees
            view = self.env['ir.ui.view'].browse(self.env['ir.model.data'].xmlid_to_res_id('project_assignees.message_user_assigned'))
            model_description = self.env['ir.model']._get(task._name).display_name
            
            for assignee in assignees:
                values = {
                    'object': task,
                    'model_description': model_description,
                    'partner_name':assignee.name_get()[0][1]
                }
                assignation_msg = view.render(values, engine='ir.qweb', minimal_qcontext=True)
                assignation_msg = self.env['mail.thread']._replace_local_links(assignation_msg)

                
                task.message_notify(
                    subject=_('You have been assigned to %s') % task.display_name,
                    body=assignation_msg,
                    partner_ids=[(4, assignee.partner_id.id)],
                    record_name=task.display_name,
                    notif_layout='mail.mail_notification_light',
                    model_description=model_description,
                )



    @api.multi
    def write(self, vals):
        # Notify only new assignees
        if 'assignee_ids' in vals:
            new_assignee_ids = vals['assignee_ids'][0][2].copy()               
            for a in self.assignee_ids:
                if a.id in new_assignee_ids:
                    new_assignee_ids.remove(a.id)
            self.subscribe_and_notify_assignees(new_assignee_ids)
        
        result = super(Task, self).write(vals)
        
        return result
    
    @api.model
    def create(self, vals):
        task = super(Task, self).create(vals)
        task.subscribe_and_notify_assignees()
        return task
    
    
    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        # keep notification of new task when creating a new task
        res = super(Task, self)._track_subtype(init_values)
        if res == 'project.mt_task_new':
            return res
        # if assignees change, notify it
        if 'assignee_ids' in init_values:
            return 'project_assignees.mt_task_assignees'
        
        return super(Task, self)._track_subtype(init_values)