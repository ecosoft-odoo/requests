# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class RequestCategory(models.Model):
    _inherit = "request.category"

    _use_approver = False  # Drop default system for base_tier_validation
