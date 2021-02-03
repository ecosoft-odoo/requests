# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RequestProductLine(models.Model):
    _inherit = "request.product.line"

    def _filter_purchase_request_line(self):
        """ Hook method """
        return self
