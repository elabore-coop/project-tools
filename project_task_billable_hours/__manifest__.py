# Copyright 2022 Elabore
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project task billable hours",
    "version": "16.0.1.0.0",
    "author": "Elabore",
    "website": "https://github.com/elabore-coop/project-tools",
    "maintainer": "Laetitia Da Costa",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "In task kanban view, display remaining billable hours instead of remaining hours",
    "description": "",
    "depends": [
        "project",
        "hr_timesheet",
        "project_working_time_task_portal"
    ],
    "data": [
        "views/project_task_views.xml",        
    ],
    "installable": True,
    "application": False,
}
