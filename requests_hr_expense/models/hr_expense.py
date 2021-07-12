# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HRExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    request_id = fields.Many2one(
        comodel_name="request.request",
        index=True,
        ondelete="restrict",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        user_id = self.env.context.get("request_owner_id")
        if user_id:
            user = self.env["res.users"].browse(user_id)
            res["employee_id"] = user.employee_id.id
        return res

    def action_open_requests(self):
        self.ensure_one()
        action = {
            "name": _("Requests"),
            "view_mode": "form",
            "res_model": "request.request",
            "res_id": self.request_id.id,
            "type": "ir.actions.act_window",
            "context": self.env.context,
        }
        return action
