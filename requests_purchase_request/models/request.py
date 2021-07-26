# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    use_pr = fields.Boolean(related="category_id.use_pr")
    purchase_request_count = fields.Integer(
        compute="_compute_purchase_request_count"
    )
    purchase_request_ids = fields.One2many(
        string="Purchase Requests",
        comodel_name="purchase.request",
        inverse_name="ref_request_id",
        copy=False,
    )

    def _get_child_amount(self):
        amount = sum(self.purchase_request_ids.mapped("estimated_cost"))
        return super()._get_child_amount() + amount

    def _ready_to_submit(self):
        if not super()._ready_to_submit():
            return False
        if not self.purchase_request_ids:
            return True
        # Ready if all PR are in To Approve state
        states = list(set(self.purchase_request_ids.mapped("state")))
        return len(states) == 1 and states[0] == "to_approve"

    def _compute_purchase_request_count(self):
        for request in self:
            request.purchase_request_count = len(request.purchase_request_ids)

    def action_view_purchase_request(self):
        self.ensure_one()
        action = {
            "name": _("Purchase Request"),
            "view_mode": "list,form",
            "res_model": "purchase.request",
            "type": "ir.actions.act_window",
            "context": {"create": False, "delete": False, "edit": True},
            "domain": [("id", "in", self.purchase_request_ids.ids)],
        }
        return action

    def action_create_purchase_request(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({"default_ref_request_id": self.id})
        action = {
            "name": _("Purchase Request"),
            "view_mode": "form",
            "res_model": "purchase.request",
            "type": "ir.actions.act_window",
            "context": ctx,
        }
        return action
