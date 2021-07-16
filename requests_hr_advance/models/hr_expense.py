# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class HRExpenseSheet(models.Model):
    _name = "hr.expense.sheet"
    _inherit = ["hr.expense.sheet", "request.doc.mixin"]
    _request_freeze_states = ["pending"]
    _doc_approved_states = ["approve"]

    # Server Actions
    def approve_expense_sheets(self):
        res = super().approve_expense_sheets()
        # Execute post AV approved action
        for rec in self.filtered(
            lambda l: l in l.ref_request_id.advance_sheet_ids
        ):
            action = rec.ref_request_id.category_id.av_approved_action_id
            action.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
        return res

    def refuse_sheet(self, reason):
        res = super().refuse_sheet(reason)
        # Execute post AV refuse action
        for rec in self.filtered(
            lambda l: l in l.ref_request_id.advance_sheet_ids
        ):
            action = rec.ref_request_id.category_id.av_rejected_action_id
            action.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
        return res


class HRExpense(models.Model):
    _inherit = "hr.expense"

    @api.depends("product_id", "company_id")
    def _compute_from_product_id_company_id(self):
        super()._compute_from_product_id_company_id()
        if self.env.context.get("request_advance_amount"):
            advance = self.filtered("advance")
            advance.update(
                {"unit_amount": self.env.context["request_advance_amount"]}
            )
