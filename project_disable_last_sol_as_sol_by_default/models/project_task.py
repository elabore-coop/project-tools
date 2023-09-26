from odoo import models

class Task(models.Model):
    _inherit = "project.task"

    def _get_last_sol_of_customer(self):
        return False