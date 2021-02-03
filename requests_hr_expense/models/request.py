# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class RequestRequest(models.Model):
    _inherit = "request.request"

    hr_expense_count = fields.Integer(compute="_compute_hr_expense_count")

    @api.depends("product_line_ids.resource_ref")
    def _compute_hr_expense_count(self):
        for request in self:
            lines = request.product_line_ids.filtered(
                lambda l: l.resource_ref
                and l.resource_ref._name == "hr.expense"
            )
            sheets = self.env["hr.expense.sheet"].browse()
            for line in lines:
                if line.resource_ref:
                    sheets |= line.resource_ref.sheet_id
            request.hr_expense_count = len(sheets)

    def _prepare_hr_expense_sheet(self):
        self.ensure_one()
        val = {
            "name": self.name,
            "company_id": self.company_id.id,
            "employee_id": self.request_owner_id.employee_id.id,
        }
        return val

    def _prepare_hr_expense_line(self, line, sheet):
        line_val = {
            "sheet_id": sheet.id,
            "employee_id": sheet.employee_id.id,
            "product_id": line.product_id.id,
            "name": line.description,
            "quantity": line.quantity,
            "unit_amount": 1111,
            "product_uom_id": line.product_uom_id.id,
        }
        return line_val

    def action_create_hr_expense(self):
        self.ensure_one()
        lines = self.product_line_ids._filter_hr_expense_line()
        if not lines:
            return
        val = self._prepare_hr_expense_sheet()
        new = self.env["hr.expense.sheet"].create(val)
        for line in lines:
            line_val = self._prepare_hr_expense_line(line, new)
            new_line = self.env["hr.expense"].create(line_val)
            line.resource_ref = "{},{}".format(
                new_line._name,
                new_line.id,
            )

    def action_open_hr_expense(self):
        self.ensure_one()
        lines = self.product_line_ids.filtered(
            lambda l: l.resource_ref and l.resource_ref._name == "hr.expense"
        )
        sheets = self.env["hr.expense.sheet"].browse()
        for line in lines:
            if line.resource_ref:
                sheets += line.resource_ref.sheet_id
        domain = [("id", "in", sheets.ids)]
        action = {
            "name": _("Expense Report"),
            "view_type": "tree",
            "view_mode": "list,form",
            "res_model": "hr.expense.sheet",
            "type": "ir.actions.act_window",
            "context": self.env.context,
            "domain": domain,
        }
        return action
