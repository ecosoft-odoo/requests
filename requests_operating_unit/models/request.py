# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class RequestOperatingUnit(models.Model):

    _inherit = "request.request"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        default=lambda self: self.env[
            "res.users"
        ].operating_unit_default_get(),
    )
