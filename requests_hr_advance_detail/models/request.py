# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RequestRequest(models.Model):
    _inherit = "request.request"

    def _prepare_advance_vals(self):
        """ Add advance lines """
        values = super()._prepare_advance_vals()
        adv_lines = []
        adv_amount = 0.0
        lines = self.product_line_ids._filter_hr_advance_line()
        if not lines:
            return values
        for line in lines:
            adv_lines.append(
                (
                    0,
                    0,
                    {
                        "name": line.description,
                        "unit_amount": line.price_subtotal,
                    },
                )
            )
            adv_amount += line.price_subtotal
        values.update({"advance_line": adv_lines, "unit_amount": adv_amount})
        return values
