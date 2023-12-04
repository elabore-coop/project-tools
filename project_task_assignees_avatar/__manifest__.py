# Copyright  Élabore (2023)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "project_task_assignees_avatar",
    "version": "14.0.1.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Boris Gallet",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Allow to show avatar of assignees to a task in kanban view",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "project",
    ],
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "views/task_kanban_avatar.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}