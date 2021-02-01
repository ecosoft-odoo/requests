# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

from odoo.addons.requests.models.request_category import CATEGORY_SELECTION


class RequestCategory(models.Model):
    _inherit = "request.category"

    has_res_type = fields.Selection(
        CATEGORY_SELECTION,
        string="Has Request Type",
        default="no",
        required=True,
    )
