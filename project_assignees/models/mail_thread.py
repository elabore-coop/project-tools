# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _message_auto_subscribe_followers(self, updated_values, default_subtype_ids):
        """ Overrides mail.thread._message_auto_subscribe_followers() only in a project task context.

        In a project task context : user(s) to notify are the assignees (field assignee_ids not user_id)
        In other context : use parent _message_auto_subscribe_followers and notify the user identify by the field user_id

        Return a list tuples containing (
          partner ID,
          subtype IDs (or False if model-based default subtypes),
          QWeb template XML ID for notification (or False is no specific
            notification is required),
          ), aka partners and their subtype and possible notification to send
        using the auto subscription mechanism linked to updated values.

        :param updated_values: see ``_message_auto_subscribe``
        :param default_subtype_ids: coming from ``_get_auto_subscription_subtypes``
        """

        if self._name == 'project.task' : 
          results = []
          assignee_ids = updated_values.get('assignee_ids')
          if assignee_ids  and len(assignee_ids)  == 1 and assignee_ids[0][0] == 6:
            user_ids = assignee_ids[0][-1]
            users = self.env['res.users'].sudo().browse(user_ids)
            if users :
              for user in users :
                try:
                    if user.active:
                        results.append((user.partner_id.id, default_subtype_ids, 'mail.message_user_assigned' if user != self.env.user else False))
                except:
                    pass
          return results
        else:
          return super()._message_auto_subscribe_followers(updated_values, default_subtype_ids)