from odoo import models, fields, api

class Project(models.Model):
    _inherit = "project.project"

    billable_remaining_hours = fields.Float(
        compute="_compute_project_billable_remaining_hours",
        string="Billable Remaining Hours",
        store=True,
        help="Total Billable remaining time (without exclude_from_sale_order timesheet lines)."
    )

    @api.depends("task_ids.billable_remaining_hours")
    def _compute_project_billable_remaining_hours(self):
        for project in self:
            project.billable_remaining_hours = sum(task.billable_remaining_hours for task in project.task_ids)
