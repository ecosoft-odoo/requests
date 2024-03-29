# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class RequestRequest(models.Model):
    _name = "request.request"
    _inherit = ["request.request", "tier.validation"]
    _state_from = ["pending"]
    _state_to = ["approved"]

    _tier_validation_manual_config = False
