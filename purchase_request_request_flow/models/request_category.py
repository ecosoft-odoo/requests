# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RequestCategory(models.Model):
    _inherit = "request.category"

    use_pr = fields.Boolean(
        string="Use Purchase Request",
        help="If checked, request document will show new create/view purchase request, "
        "user can create new purchase_request which is considered part of this request",
    )
    pr_approved_action_id = fields.Many2one(
        comodel_name="ir.actions.server",
        string="PR Approved Action",
        domain=[
            ("usage", "=", "ir_actions_server"),
            ("model_id.model", "=", "request.request"),
        ],
        help="This server action is trigger after PR is approved",
    )
    pr_rejected_action_id = fields.Many2one(
        comodel_name="ir.actions.server",
        string="PR Rejected Action",
        domain=[
            ("usage", "=", "ir_actions_server"),
            ("model_id.model", "=", "request.request"),
        ],
        help="This server action is trigger after PR is rejected",
    )

    def _has_child_docs(self):
        return super()._has_child_docs() or self.use_pr
