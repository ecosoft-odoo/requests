# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class RequestCategory(models.Model):
    _inherit = "request.category"

    _use_approver = False  # Drop default system for base_tier_validation

    def _compute_request_to_validate_count(self):
        """ Method overwrite """
        domain = [
            ("state", "=", "pending"),
            (
                "reviewer_ids",
                "=",
                self.env.user.id,
            ),  # Changed from approver_id
        ]
        requests_data = self.env["request.request"].read_group(
            domain, ["category_id"], ["category_id"]
        )
        requests_mapped_data = {
            data["category_id"][0]: data["category_id_count"]
            for data in requests_data
        }
        for category in self:
            category.request_to_validate_count = requests_mapped_data.get(
                category.id, 0
            )
