# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, exceptions, fields, models


class RequestOperatingUnit(models.Model):

    _inherit = "request.request"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        default=lambda self: self.env[
            "res.users"
        ].operating_unit_default_get(),
    )

    @api.onchange("approver_ids", "operating_unit_id")
    def _check_approver_operating_unit(self):
        for r in self.approver_ids:
            if (
                self.operating_unit_id
                not in r.user_id.sudo().operating_unit_ids
            ):
                raise exceptions.ValidationError(
                    _(
                        "Approver '{}' is not in operating unit".format(
                            r.user_id.name
                        )
                    )
                )
