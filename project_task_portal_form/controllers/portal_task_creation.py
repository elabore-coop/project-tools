# Copyright 2020 Lokavaluto ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalTaskCreation(CustomerPortal):
    _TASK_CREATION_FIELDS = [
        "name",
        "service_id",
        "request_type_id",
        "small_description",
        "access",
        "bug_report",
        "priority",
    ]

    # Variable to update to add other fields in child classes
    _EXTRA_FIELDS = []

    def _taskform_get_page_view_values(self, partner, access_token, **kwargs):
        values = {
            "page_name": "portal_task_form",
            "partner": partner,
        }
        return self._get_page_view_values(
            partner,
            access_token,
            values,
            "my_task_creation_history",
            False,
            **kwargs
        )

    def _get_task_priorities(self):
        priorities = []
        for id, name in request.env['project.task']._fields['priority'].selection:
            value = {
                "id": id,
                "name": name
            }
            priorities.append(value)
        return priorities
    
    @http.route(
        ["/task/form"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_task_creation(self, access_token=None, redirect=None, **kw):
        values = self._task_get_page_view_values(request.env.user.partner_id, access_token, **kw)
        request_types = request.env["request.type"].sudo().search([])
        task_services = request.env["task.service"].sudo().search([])
        priorities = self._get_task_priorities()
        error = dict()
        error_message = []
        values.update(
            {
                "request_types": request_types,
                "task_services": task_services,
                "priorities": priorities,
                "error": error,
                "error_message": error_message,
            }
        )
        return request.render("project_task_portal_form.portal_task_creation_form", values)

    def _compute_form_data(self, data):
        values = {}
        for field in self._TASK_CREATION_FIELDS:
            if data.get(field):
                values[field] = data.pop(field)
        for field in self._EXTRA_FIELDS:
            if data.get(field):
                values[field] = data.pop(field)
        description = ""
        if values.get("small_description", False):
            description = description + "<b>DESCRIPTION:</b><br/>" + values["small_description"] 
        if values.get("access", False):
            description = description + "<br/><br/><b>ACCESS:</b><br/>" + values["access"] 
        if values.get("bug_report", False):
            description = description + "<br/><br/><b>BUG REPORT:</b><br/>" + values["bug_report"]
        values["description"] = description
        values["attachments"] = request.httprequest.files.getlist("attachment")        
        return values

    @http.route(
        ["/task/create"],
        type="http",
        auth="public",
        methods=['POST'],
        website=True,
    )
    def create_task(self, **kwargs):
        # Get form values
        user = request.env.user
        values = self._compute_form_data(kwargs)
        values["project_id"] = user.default_project_id.id
        values["partner_id"] = user.partner_id.id
        values["user_id"] = user.id

        # Create task
        task_id = request.env["project.task"].create(values)

        # Add attachments
        for file in values.get("attachments", False):
            attachment_value = {
                    'name': file.filename,
                    'datas': base64.encodestring(file.read()),
                    'datas_fname': file.filename,
                    'res_model': "project.task",
                    'res_id': task_id,
                }
            request.env['ir.attachment'].sudo().create(attachment_value)
        return request.render("project_task_portal_form.portal_task_created", {})
