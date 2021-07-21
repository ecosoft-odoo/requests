# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    use_av = fields.Boolean(related="category_id.use_av")
    hr_advance_count = fields.Integer(compute="_compute_hr_advance_count")
    expense_sheet_ids = fields.One2many(
        domain=[("advance", "=", False)],
    )
    advance_sheet_ids = fields.One2many(
        string="Advance Sheets",
        comodel_name="hr.expense.sheet",
        inverse_name="ref_request_id",
        domain=[("advance", "=", True)],
        copy=False,
    )

    def _compute_hr_advance_count(self):
        for request in self:
            request.hr_advance_count = len(request.advance_sheet_ids)

    def action_view_advance(self):
        self.ensure_one()
        action = {
            "name": _("Advance Sheet"),
            "view_mode": "list,form",
            "res_model": "hr.expense.sheet",
            "type": "ir.actions.act_window",
            "context": {"create": False, "edit": False},
            "domain": [("id", "in", self.advance_sheet_ids.ids)],
        }
        return action

    def action_create_advance(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        advance = self.env.ref(
            "hr_expense_advance_clearing.product_emp_advance"
        )
        ctx.update(
            {
                "default_ref_request_id": self.id,
                # Additiona, for advance
                "default_expense_line_ids": [
                    (
                        0,
                        0,
                        {
                            "advance": True,
                            "product_id": advance.id,
                        },
                    )
                ],
                "request_advance_amount": self.amount,
            }
        )
        action = {
            "name": _("Advance Sheet"),
            "view_mode": "form",
            "res_model": "hr.expense.sheet",
            "type": "ir.actions.act_window",
            "context": ctx,
        }
        return action
