# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class RequestDocMixin(models.AbstractModel):
    _name = "request.doc.mixin"
    _description = "Child doc of the request"
    _request_freeze_states = (
        []
    )  # Document is freezed, if request is in these states
    _doc_approved_states = (
        []
    )  # Document can move to this approved state, only by request

    ref_request_id = fields.Many2one(
        comodel_name="request.request",
        index=True,
        ondelete="restrict",
    )

    def write(self, vals):
        for rec in self.filtered("ref_request_id"):
            # Affect from _request_freeze_states
            if rec.ref_request_id.state in self._request_freeze_states:
                raise ValidationError(
                    _(
                        "This document is part of %s which is under validation.\n"
                        "No changes allowed!"
                    )
                    % rec.ref_request_id.display_name
                )
            # Affect from _doc_states_by_request
            if self._doc_approved_states and not self.env.context.get(
                "request_action_approve"
            ):
                if vals.get("state") in self._doc_approved_states:
                    raise ValidationError(
                        _(
                            "This action will be approved when Request %s is approved."
                        )
                        % rec.ref_request_id.display_name
                    )
        return super().write(vals)

    @api.onchange("ref_request_id")
    def _onchange_ref_rqeuest_set_defaults(self):
        vals = self._prepare_defaults()
        self.update(vals)

    def _prepare_defaults(self):
        """ Hook method to prepare default for creating doc """
        return {}

    def action_open_requests(self):
        self.ensure_one()
        action = {
            "name": _("Requests"),
            "view_mode": "form",
            "res_model": "request.request",
            "res_id": self.ref_request_id.id,
            "type": "ir.actions.act_window",
            "context": self.env.context,
        }
        return action


class RequestDocLineMixin(models.AbstractModel):
    _name = "request.doc.line.mixin"
    _description = "Child doc line of the request"

    ref_request_id = fields.Many2one(
        comodel_name="request.request",
    )

    @api.onchange("ref_request_id")
    def _onchange_ref_rqeuest_set_defaults(self):
        vals = self._prepare_defaults()
        self.update(vals)

    def _prepare_defaults(self):
        """ Hook method to prepare default for creating doc line """
        return {}
