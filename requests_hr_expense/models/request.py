# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    use_ex = fields.Boolean(related="category_id.use_ex")
    hr_expense_count = fields.Integer(compute="_compute_hr_expense_count")
    expense_sheet_ids = fields.One2many(
        string="Expense Sheets",
        comodel_name="hr.expense.sheet",
        inverse_name="ref_request_id",
        copy=False,
    )

    def _get_child_amount(self):
        amount = sum(self.expense_sheet_ids.mapped("total_amount"))
        return super()._get_child_amount() + amount

    def _compute_hr_expense_count(self):
        for request in self:
            request.hr_expense_count = len(request.expense_sheet_ids)

    def action_view_expense(self):
        self.ensure_one()
        action = {
            "name": _("Expense Sheet"),
            "view_mode": "list,form",
            "res_model": "hr.expense.sheet",
            "type": "ir.actions.act_window",
            "context": {"create": False, "delete": False, "edit": True},
            "domain": [("id", "in", self.expense_sheet_ids.ids)],
        }
        return action

    def action_create_expense(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({"default_ref_request_id": self.id})
        action = {
            "name": _("Expense Sheet"),
            "view_mode": "form",
            "res_model": "hr.expense.sheet",
            "type": "ir.actions.act_window",
            "context": ctx,
        }
        return action
