# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RequestProductLine(models.Model):
    _inherit = "request.product.line"

    res_type = fields.Selection(
        selection=[
            ("pr", "Purchase"),
            ("ex", "Expense"),
        ],
        string="Type",
        help="Line's type will ensure different document get created",
    )

    def _filter_hr_expense_line(self):
        lines = (
            super()
            ._filter_hr_expense_line()
            .filtered(lambda l: l.res_type == "ex")
        )
        return lines

    def _filter_purchase_request_line(self):
        lines = (
            super()
            ._filter_purchase_request_line()
            .filtered(lambda l: l.res_type == "pr")
        )
        return lines
