# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class RequestProductLine(models.Model):
    _inherit = "request.product.line"

    def _filter_purchase_request_line(self):
        """ Hook method """
        return self
