# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    use_expense = fields.Boolean(related="category_id.use_expense")
    hr_expense_count = fields.Integer(compute="_compute_hr_expense_count")
    expense_sheet_ids = fields.One2many(
        string="Expense Sheets",
        comodel_name="hr.expense.sheet",
        inverse_name="request_id",
        copy=False,
    )

    def _compute_hr_expense_count(self):
        for request in self:
            request.hr_expense_count = len(request.expense_sheet_ids)

    def action_view_expense(self):
        self.ensure_one()
        action = {
            "name": _("Expense Report"),
            "view_mode": "list,form",
            "res_model": "hr.expense.sheet",
            "type": "ir.actions.act_window",
            "context": {"create": False, "edit": False},
            "domain": [("id", "in", self.expense_sheet_ids.ids)],
        }
        return action

    def action_create_expense(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "active_model": self._name,
                "active_id": self.id,
            }
        )
        action = self.category_id.expense_action_id.with_context(ctx)
        return action.sudo().run()
