# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RequestCategory(models.Model):
    _inherit = "request.category"

    use_purchase_request = fields.Boolean(
        string="Use Purchase Request",
        help="If checked, request document will show new create/view purchase request, "
        "user can create new purchase_request which is considered part of this request",
    )
    purchase_request_action_id = fields.Many2one(
        comodel_name="ir.actions.server",
        string="On Create PR",
        domain=[
            ("usage", "=", "ir_actions_server"),
            ("model_id.model", "=", "request.request"),
        ],
        help="This server action is trigger on click button Create Purchase Request",
    )
