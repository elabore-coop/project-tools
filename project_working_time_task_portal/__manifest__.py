# Copyright 2022 Boris Gallet ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "project_working_time_task_portal",
    "version": "14.0.2.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Boris Gallet",
    "license": "AGPL-3",
    "category": "tools",
    "summary": "add billable planned hours and billable remaining hours in the task portal view so the portal user only see billable timesheet lines",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "project",
        "sale_timesheet_line_exclude"
    ],
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "views/assets.xml",
        "views/hr_timesheet_portal.xml",
        "views/hr_timesheet_view_task_form2.xml"
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": ["static/src/css/main.css"],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}