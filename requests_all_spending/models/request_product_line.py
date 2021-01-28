# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class RequestProductLine(models.Model):
    _inherit = "request.product.line"

    res_type = fields.Selection(
        selection=[
            ("ex", "EX"),
            ("pr", "PR"),
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
