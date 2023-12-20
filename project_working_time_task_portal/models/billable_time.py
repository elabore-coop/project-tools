from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare


class Task(models.Model):
    _inherit = "project.task"

    billable_effective_hours = fields.Float(
        compute="_compute_billable_effective_hours",
        string="Billable Effective Hours",
        store=True,
        compute_sudo=True,
    )

    non_billable_effective_hours = fields.Float(
        compute="_compute_non_billable_effective_hours",
        string="Non Billable Effective Hours",
        store=True,
    )

    billable_remaining_hours = fields.Float(
        compute="_compute_billable_remaining_hours",
        string="Billable Remaining Hours",
        store=True,
        help="Total Billable remaining time (without exclude_from_sale_order timesheet lines), can be re-estimated periodically by the assignee of the task."
    )

    billable_progress = fields.Float(
        compute="_compute_billable_progress_hours",
        string="Billable Progress",
        store=True,
        group_operator="avg",
    )

    subtask_billable_effective_hours = fields.Float(
        compute="_compute_subtask_billable_effective_hours",
        string="Subtask Billable Effective Hours",
        store=True,
        compute_sudo=True,
    )

    @api.depends('timesheet_ids.unit_amount')
    def _compute_billable_effective_hours(self):
        if not any(self._ids):
            for task in self:
                filtered_timesheets = task.timesheet_ids.filtered(lambda t: not t.exclude_from_sale_order)
                task.billable_effective_hours = sum(filtered_timesheets.mapped('unit_amount'))
            return
      
        timesheet_read_group = self.env['account.analytic.line'].read_group(
            [('task_id', 'in', self.ids), ('exclude_from_sale_order', '=', False)], # We exclude the lines (timesheet) which are excluded from billing
            ['unit_amount', 'task_id'], 
            ['task_id']
        )

        timesheets_per_task = {res['task_id'][0]: res['unit_amount'] for res in timesheet_read_group}
        for task in self:
            task.billable_effective_hours = timesheets_per_task.get(task.id, 0.0)

    @api.depends('effective_hours','billable_effective_hours')
    def _compute_non_billable_effective_hours(self):
        for task in self:
            task.non_billable_effective_hours = task.effective_hours - task.billable_effective_hours

    @api.depends('billable_effective_hours', 'subtask_billable_effective_hours', 'planned_hours')
    def _compute_billable_remaining_hours(self):
        for task in self:
            task.billable_remaining_hours = task.planned_hours - task.billable_effective_hours - task.subtask_billable_effective_hours


    @api.depends('child_ids.billable_effective_hours', 'child_ids.subtask_billable_effective_hours')
    def _compute_subtask_billable_effective_hours(self):
        for task in self:
            task.subtask_billable_effective_hours = sum(child_task.billable_effective_hours + child_task.subtask_billable_effective_hours for child_task in task.child_ids)

    @api.depends('billable_effective_hours', 'subtask_billable_effective_hours', 'planned_hours')
    def _compute_billable_progress_hours(self):
        for task in self:
            if (task.planned_hours > 0.0):
                task_total_hours = task.billable_effective_hours + task.subtask_billable_effective_hours
                if float_compare(task_total_hours, task.planned_hours, precision_digits=2) >= 0:
                    task.billable_progress = 100
                else:
                    task.billable_progress = round(100.0 * task_total_hours / task.planned_hours, 2)
            else:
                task.billable_progress = 0.0