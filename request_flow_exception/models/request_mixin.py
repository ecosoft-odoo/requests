# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class RequestDocMixin(models.AbstractModel):
    _inherit = "request.doc.mixin"

    @api.constrains("state")
    def _trigger_ready_to_submit(self):
        super()._trigger_ready_to_submit()
        # To show exception on request
        requests = self.filtered("ref_request_id").mapped("ref_request_id")
        requests.filtered(lambda l: l.state == "draft").detect_exceptions()
