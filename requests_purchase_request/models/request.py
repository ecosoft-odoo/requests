# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    purchase_request_count = fields.Integer(
        compute="_compute_purchase_request_count"
    )
    purchase_request_ids = fields.One2many(
        string="Purchase Requests",
        comodel_name="purchase.request",
        inverse_name="request_id",
        copy=True,
    )

    @api.depends("product_line_ids.resource_ref")
    def _compute_purchase_request_count(self):
        for request in self:
            request.purchase_request_count = len(request.purchase_request_ids)

    def _prepare_purchase_request(self):
        self.ensure_one()
        val = {
            "origin": self.name,
            "company_id": self.company_id.id,
            "requested_by": self.request_owner_id.id,
            "description": self.reason,
            "request_id": self.id,
        }
        return val

    def _prepare_purchase_request_line(self, line, purchase_request):
        line_val = {
            "request_id": purchase_request.id,
            "product_id": line.product_id.id,
            "name": line.product_id.display_name,
            "product_qty": line.quantity,
            "product_uom_id": line.product_uom_id.id,
            "estimated_cost": line.price_subtotal,
        }
        return line_val

    def action_create_purchase_request(self):
        self.ensure_one()
        lines = self.product_line_ids._filter_purchase_request_line()
        if not lines:
            return
        val = self.env["purchase.request"].default_get(["name"])
        val.update(self._prepare_purchase_request())
        new = self.env["purchase.request"].create(val)
        for line in lines:
            line_val = self._prepare_purchase_request_line(line, new)
            new_line = self.env["purchase.request.line"].create(line_val)
            line.resource_ref = "{},{}".format(
                new_line._name,
                new_line.id,
            )

    def action_open_purchase_request(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.pop("default_state", False)
        if self.state != "new":
            ctx.update({"create": False, "edit": False})
        action = {
            "name": _("Purchase Request"),
            "view_type": "tree",
            "view_mode": "list,form",
            "res_model": "purchase.request",
            "type": "ir.actions.act_window",
            "context": ctx,
            "domain": [("id", "in", self.purchase_request_ids.ids)],
        }
        return action
