# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseRquest(models.Model):
    _name = "purchase.request"
    _inherit = ["purchase.request", "request.doc.mixin"]
    _request_freeze_states = ["pending"]
    _doc_approved_states = ["approved"]

    def _compute_child_amount(self):
        for rec in self:
            amount = sum(rec.purchase_request_ids.mapped("estimated_cost"))
            rec.child_amount += amount

    def _prepare_defaults(self):
        res = super()._prepare_defaults()
        request = self.ref_request_id
        lines = []
        for line in request.product_line_ids:
            vals = {
                "product_id": line.product_id.id,
                "name": line.description,
                "product_qty": line.quantity,
                "estimated_cost": line.price_subtotal,
            }
            lines.append((0, 0, vals))
        res.update(
            {
                "origin": request.name,
                "requested_by": request.requested_by.id,
                "assigned_to": request.approver_id.id,
                "date_start": request.date,
                "description": request.reason,
                "line_ids": lines,
            }
        )
        return res

    # Server Actions
    def button_approved(self):
        res = super().button_approved()
        # Execute post PR approved action
        for rec in self.filtered(
            lambda l: l in l.ref_request_id.purchase_request_ids
        ):
            action = rec.ref_request_id.category_id.pr_approved_action_id
            action.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
        return res

    def button_rejected(self):
        res = super().button_rejected()
        # Execute post PR rejected action
        for rec in self.filtered(
            lambda l: l in l.ref_request_id.purchase_request_ids
        ):
            action = rec.ref_request_id.category_id.pr_rejected_action_id
            action.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
        return res


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    _inherit = ["purchase.request.line", "request.doc.line.mixin"]

    ref_request_id = fields.Many2one(
        related="request_id.ref_request_id",
    )

    def _prepare_defaults(self):
        res = super()._prepare_defaults()
        return res
