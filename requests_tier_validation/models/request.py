# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models
from odoo.exceptions import UserError


class RequestRequest(models.Model):
    _name = "request.request"
    _inherit = ["request.request", "tier.validation"]
    _state_from = ["pending"]
    _state_to = ["approved"]

    _tier_validation_manual_config = False

    state = fields.Selection(
        compute=False,
    )

    def action_confirm(self):
        res = super().action_confirm()
        self.write({"state": "pending"})
        return res

    def action_approve(self, approver=None):
        res = super().action_approve()
        self.write({"state": "approved"})
        return res

    def action_refuse(self, approver=None):
        res = super().action_refuse()
        self.write({"state": "refused"})
        return res

    def action_withdraw(self, approver=None):
        res = super().action_withdraw()
        self.write({"state": "pending"})
        return res

    def action_draft(self):
        res = super().action_draft()
        self.write({"state": "new"})
        return res

    def action_cancel(self):
        res = super().action_cancel()
        if self.filtered("can_review"):
            raise UserError(_("Workflow started, cancel is not allowed."))
        self.write({"state": "cancel"})
        return res

    def _compute_user_status(self):
        """ Calculate user_status for case tier validation is used """
        for request in self:
            if request.need_validation:
                if request.state == "new":
                    request.user_status = "new"
                elif request.state == "pending":
                    request.user_status = False
            else:
                if request.state == "pending":
                    if request.can_review:
                        request.user_status = False
                    else:
                        request.user_status = "pending"
                elif request.state == "cancel":
                    request.user_status = "cancel"
                else:
                    request.user_status = "new"
