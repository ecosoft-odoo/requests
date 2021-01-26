# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource


CATEGORY_SELECTION = [
    ("required", "Required"),
    ("optional", "Optional"),
    ("no", "None"),
]


class RequestCategory(models.Model):
    _name = "request.category"
    _description = "Request Category"
    _order = "sequence"

    _check_company_auto = True

    def _get_default_image(self):
        default_image_path = get_module_resource(
            "requests", "static/src/img", "clipboard-check-solid.svg"
        )
        return base64.b64encode(open(default_image_path, "rb").read())

    name = fields.Char(string="Name", translate=True, required=True)
    company_id = fields.Many2one(
        "res.company",
        "Company",
        copy=False,
        required=True,
        index=True,
        default=lambda s: s.env.company,
    )
    active = fields.Boolean(default=True)
    sequence = fields.Integer(string="Sequence")
    description = fields.Char(string="Description", translate=True)
    image = fields.Binary(string="Image", default=_get_default_image)
    has_date = fields.Selection(
        CATEGORY_SELECTION, string="Has Date", default="no", required=True
    )
    has_period = fields.Selection(
        CATEGORY_SELECTION, string="Has Period", default="no", required=True
    )
    has_quantity = fields.Selection(
        CATEGORY_SELECTION, string="Has Quantity", default="no", required=True
    )
    has_amount = fields.Selection(
        CATEGORY_SELECTION, string="Has Amount", default="no", required=True
    )
    has_reference = fields.Selection(
        CATEGORY_SELECTION,
        string="Has Reference",
        default="no",
        required=True,
        help="An additional reference that should be specified on the request.",
    )
    has_partner = fields.Selection(
        CATEGORY_SELECTION, string="Has Contact", default="no", required=True
    )
    has_payment_method = fields.Selection(
        CATEGORY_SELECTION, string="Has Payment", default="no", required=True
    )
    has_location = fields.Selection(
        CATEGORY_SELECTION, string="Has Location", default="no", required=True
    )
    has_product = fields.Selection(
        CATEGORY_SELECTION,
        string="Has Product",
        default="no",
        required=True,
        help="Additional products that should be specified on the request.",
    )
    requirer_document = fields.Selection(
        [("required", "Required"), ("optional", "Optional")],
        string="Documents",
        default="optional",
        required=True,
    )
    request_minimum = fields.Integer(
        string="Minimum Request", default="1", required=True
    )
    request_type = fields.Selection(
        string="Request Type",
        selection=[],
        help="Allows you to define which documents you would like to create once the request has been approved",
    )
    is_manager_approver = fields.Boolean(
        string="Employee's Manager",
        help="Automatically add the manager as approver on the request.",
    )
    user_ids = fields.Many2many(
        "res.users",
        string="Approvers",
        check_company=True,
        domain="[('company_ids', 'in', company_id)]",
    )
    request_to_validate_count = fields.Integer(
        "Number of requests to validate", compute="_compute_request_to_validate_count"
    )
    automated_sequence = fields.Boolean(
        "Automated Sequence?",
        help="If checked, the Request Requests will have an automated generated name based on the given code.",
    )
    sequence_code = fields.Char(string="Code")
    sequence_id = fields.Many2one(
        "ir.sequence", "Reference Sequence", copy=False, check_company=True
    )

    def _compute_request_to_validate_count(self):
        domain = [
            ("request_status", "=", "pending"),
            ("approver_ids.user_id", "=", self.env.user.id),
        ]
        requests_data = self.env["request.request"].read_group(
            domain, ["category_id"], ["category_id"]
        )
        requests_mapped_data = dict(
            (data["category_id"][0], data["category_id_count"])
            for data in requests_data
        )
        for category in self:
            category.request_to_validate_count = requests_mapped_data.get(
                category.id, 0
            )

    @api.model
    def create(self, vals):
        if vals.get("automated_sequence"):
            sequence = self.env["ir.sequence"].create(
                {
                    "name": _("Sequence") + " " + vals["sequence_code"],
                    "padding": 5,
                    "prefix": vals["sequence_code"],
                    "company_id": vals.get("company_id"),
                }
            )
            vals["sequence_id"] = sequence.id

        request_category = super().create(vals)
        return request_category

    def write(self, vals):
        if "sequence_code" in vals:
            for request_category in self:
                sequence_vals = {
                    "name": _("Sequence") + " " + vals["sequence_code"],
                    "padding": 5,
                    "prefix": vals["sequence_code"],
                }
                if request_category.sequence_id:
                    request_category.sequence_id.write(sequence_vals)
                else:
                    sequence_vals["company_id"] = vals.get(
                        "company_id", request_category.company_id.id
                    )
                    sequence = self.env["ir.sequence"].create(sequence_vals)
                    request_category.sequence_id = sequence
        if "company_id" in vals:
            for request_category in self:
                if request_category.sequence_id:
                    request_category.sequence_id.company_id = vals.get("company_id")
        return super().write(vals)

    def create_request(self):
        self.ensure_one()
        # If category uses sequence, set next sequence as name
        # (if not, set category name as default name).
        if self.automated_sequence:
            name = self.sequence_id.next_by_id()
        else:
            name = self.name
        return {
            "type": "ir.actions.act_window",
            "res_model": "request.request",
            "views": [[False, "form"]],
            "context": {
                "form_view_initial_mode": "edit",
                "default_name": name,
                "default_category_id": self.id,
                "default_request_owner_id": self.env.user.id,
                "default_request_status": "new",
            },
        }
