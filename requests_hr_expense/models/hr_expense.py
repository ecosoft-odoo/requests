# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HRExpenseSheet(models.Model):
    _name = "hr.expense.sheet"
    _inherit = ["hr.expense.sheet", "request.doc.mixin"]
    _request_freeze_states = ["pending"]
    _doc_approved_states = ["approve"]

    def _prepare_defaults(self):
        res = super()._prepare_defaults()
        request = self.ref_request_id
        lines = []
        for line in request.product_line_ids:
            vals = {
                "product_id": line.product_id.id,
                "name": line.description,
                "quantity": line.quantity,
                "unit_amount": line.price_unit,
                "date": request.date,
            }
            lines.append((0, 0, vals))
        res.update(
            {
                "employee_id": request.requested_by.employee_id.id,
                "user_id": request.approver_id.id,
                "expense_line_ids": lines,
                "name": request.reason,
            }
        )
        return res

    # Server Actions
    def approve_expense_sheets(self):
        res = super().approve_expense_sheets()
        # Execute post EX approved action
        for rec in self.filtered(
            lambda l: l in l.ref_request_id.expense_sheet_ids
        ):
            action = rec.ref_request_id.category_id.ex_approved_action_id
            action.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
        return res

    def refuse_sheet(self, reason):
        res = super().refuse_sheet(reason)
        # Execute post EX refuse action
        for rec in self.filtered(
            lambda l: l in l.ref_request_id.expense_sheet_ids
        ):
            action = rec.ref_request_id.category_id.ex_rejected_action_id
            action.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
        return res


class HRExpense(models.Model):
    _name = "hr.expense"
    _inherit = ["hr.expense", "request.doc.line.mixin"]

    ref_request_id = fields.Many2one(
        related="sheet_id.ref_request_id",
    )

    def _prepare_defaults(self):
        res = super()._prepare_defaults()
        return res
