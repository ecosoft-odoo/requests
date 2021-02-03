# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    has_res_type = fields.Selection(related="category_id.has_res_type")
