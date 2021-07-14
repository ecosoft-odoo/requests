# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RequestCategory(models.Model):
    _inherit = "request.category"

    use_expense = fields.Boolean(
        string="Use Expense",
        help="If checked, request document will show new create/view expense sheet, "
        "user can create new expense sheet which is considered part of this request",
    )
    expense_action_id = fields.Many2one(
        comodel_name="ir.actions.server",
        string="On Create EX",
        domain=[
            ("usage", "=", "ir_actions_server"),
            ("model_id.model", "=", "request.request"),
        ],
        help="This server action is trigger on click button Create Expense",
    )
