# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    has_res_type = fields.Selection(related="category_id.has_res_type")
