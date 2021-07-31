# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RequestCategory(models.Model):
    _inherit = "request.category"

    use_ex = fields.Boolean(
        string="Use Expense",
        help="If checked, request document will show new create/view expense, "
        "user can create new hr_expense_sheet which is considered part of this request",
    )
    ex_approved_action_id = fields.Many2one(
        comodel_name="ir.actions.server",
        string="EX Approved Action",
        domain=[
            ("usage", "=", "ir_actions_server"),
            ("model_id.model", "=", "request.request"),
        ],
        help="This server action is trigger after EX is approved",
    )
    ex_rejected_action_id = fields.Many2one(
        comodel_name="ir.actions.server",
        string="EX Rejected Action",
        domain=[
            ("usage", "=", "ir_actions_server"),
            ("model_id.model", "=", "request.request"),
        ],
        help="This server action is trigger after EX is rejected",
    )

    def _has_child_docs(self):
        return super()._has_child_docs() or self.use_ex
