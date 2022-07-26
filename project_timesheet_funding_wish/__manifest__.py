# Copyright 2022 Stéphan Sainléger (Elabore)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "project_timesheet_funding_wish",
    "version": "14.0.1.0.0",
    "author": "Elabore",
    "website": "https://github.com/elabore-coop/project-tools",
    "maintainer": "Stéphan Sainléger",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Add a funding wish select field to timesheet line.",
    "description": """
   :image: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
==============================
project_timesheet_funding_wish
==============================

Add a funding wish select field to timesheet line.

Installation
============

Use Odoo normal procedure to install add-ons to install
``project_timesheet_funding_wish``.

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `our issues website <https://github.com/elabore-coop/project-tools/issues>`_. In
case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.

Credits
=======

Images
------
* Elabore: `Icon <https://elabore.coop/web/image/res.company/1/logo?unique=f3db262>`_.

Contributors
------------
* Stéphan Sainléger <https://github.com/stephansainleger>
* Valentin Lab <valentin.lab@kalysto.org>
* Nicolas Jeudy <https://github.com/njeudy>

Funders
-------
The development of this module has been financially supported by:
* Elabore (https://elabore.coop)


Maintainer
----------
This module is maintained by Elabore.

""",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "hr_timesheet",
    ],
    "qweb": [
        # "static/src/xml/*.xml",
    ],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "views/hr_timesheet.xml",
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
