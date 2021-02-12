# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RequestRequest(models.Model):
    _inherit = "request.request"

    def _prepare_advance_vals(self):
        """ Add advance lines """
        values = super()._prepare_advance_vals()
        adv_lines = []
        for request_line in self.product_line_ids:
            adv_lines.append(
                (
                    0,
                    0,
                    {
                        "name": request_line.description,
                        "unit_amount": request_line.price_subtotal,
                    },
                )
            )
        values.update({"advance_line": adv_lines})
        return values
