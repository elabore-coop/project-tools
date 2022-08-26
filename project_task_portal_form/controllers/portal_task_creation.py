# Copyright 2020 Lokavaluto ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
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
        partner = request.env.user.partner_id
        values = self._task_get_page_view_values(partner, access_token, **kw)
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
        return values

    @http.route(
        ["/task/create"],
        type="http",
        auth="public",
        website=True,
    )
    def create_task(self, **kwargs):
        # Get form values
        user = request.env.user
        values = self._compute_form_data(kwargs)
        values["project_id"] = user.default_project_id.id
        values["partner_id"] = user.partner_id.id
        values["user_id"] = None

        # Create task
        request.env["project.task"].create(values)
        return request.render("project_task_portal_form.portal_task_created", {})
