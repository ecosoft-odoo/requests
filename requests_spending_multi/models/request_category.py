# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.requests.models.request_category import CATEGORY_SELECTION


class RequestCategory(models.Model):
    _inherit = "request.category"

    has_res_type = fields.Selection(
        CATEGORY_SELECTION,
        string="Has Request Type",
        default="no",
        required=True,
    )
    default_res_type = fields.Selection(
        selection=[
            ("pr", "Purchase"),
            ("ex", "Expense"),
            ("av", "Advance"),
        ],
        string="Default Type",
    )
