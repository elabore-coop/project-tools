# Copyright 2020 Lokavaluto ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomCustomerPortal(CustomerPortal):
    @route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        self.OPTIONAL_BILLING_FIELDS.append("average_acceptable_time")

        response = super(CustomCustomerPortal, self).account(redirect, **post)
        
        if post and request.httprequest.method == "POST":
            error, error_message = self.details_form_validate(post)
            if not error:
                user = request.env.user
                if user.default_project_id and post["average_acceptable_time"]:
                    user.default_project_id.average_acceptable_time = post["average_acceptable_time"]
                    
        return response
