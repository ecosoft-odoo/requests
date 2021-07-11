# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class PurchaseRquest(models.Model):
    _inherit = "purchase.request"

    requests_id = fields.Many2one(
        comodel_name="request.request",
        index=True,
        ondelete="restrict",
    )

    def action_open_requests(self):
        self.ensure_one()
        action = {
            "name": _("Requests"),
            "view_mode": "form",
            "res_model": "request.request",
            "res_id": self.requests_id.id,
            "type": "ir.actions.act_window",
            "context": self.env.context,
        }
        return action
