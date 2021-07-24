# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RequestRequest(models.Model):
    _name = "request.request"
    _description = "Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    _check_company_auto = True

    @api.model
    def _read_group_state(self, states, domain, order):
        return dict(self._fields["state"].selection).keys()

    name = fields.Char(string="Request Subject", tracking=True)
    category_id = fields.Many2one(
        "request.category", string="Category", required=True
    )
    use_approver = fields.Boolean(related="category_id.use_approver")
    has_child = fields.Boolean(related="category_id.has_child")
    child_amount = fields.Float(
        string="Total Documents' Amount",
        compute="_compute_child_amount",
        help="Sum of all child document's amount (for extended module)",
    )
    approver_id = fields.Many2one(
        comodel_name="res.users",
        string="Approver",
        check_company=True,
        domain="[('id', '!=', requested_by)]",
    )
    company_id = fields.Many2one(
        string="Company",
        related="category_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    date = fields.Datetime(string="Date")
    date_start = fields.Datetime(string="Date start")
    date_end = fields.Datetime(string="Date end")
    quantity = fields.Float(string="Quantity")
    location = fields.Char(string="Location")
    date_confirmed = fields.Datetime(string="Date Confirmed")
    partner_id = fields.Many2one(
        "res.partner", string="Contact", check_company=True
    )
    reference = fields.Char(string="Reference")
    amount = fields.Float(string="Amount")
    reason = fields.Text(string="Reasons")
    remark = fields.Html(string="Remarks")
    state = fields.Selection(
        [
            ("draft", "To Submit"),
            ("pending", "Submitted"),
            ("approved", "Approved"),
            ("refused", "Refused"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        tracking=True,
        group_expand="_read_group_state",
    )
    requested_by = fields.Many2one(
        "res.users",
        string="Request Owner",
        required=True,
        check_company=True,
        domain="[('company_ids', 'in', company_id)]",
        default=lambda self: self.env.user,
    )
    has_access_to_request = fields.Boolean(
        string="Has Access To Request",
        compute="_compute_has_access_to_request",
    )
    attachment_number = fields.Integer(
        "Number of Attachments", compute="_compute_attachment_number"
    )
    product_line_ids = fields.One2many(
        "request.product.line", "request_id", check_company=True
    )
    has_date = fields.Selection(related="category_id.has_date")
    has_period = fields.Selection(related="category_id.has_period")
    has_quantity = fields.Selection(related="category_id.has_quantity")
    has_amount = fields.Selection(related="category_id.has_amount")
    has_reference = fields.Selection(related="category_id.has_reference")
    has_partner = fields.Selection(related="category_id.has_partner")
    has_payment_method = fields.Selection(
        related="category_id.has_payment_method"
    )
    has_location = fields.Selection(related="category_id.has_location")
    has_product = fields.Selection(related="category_id.has_product")
    has_document = fields.Selection(related="category_id.has_document")
    # request_minimum = fields.Integer(related="category_id.request_minimum")
    approved_action_id = fields.Many2one(
        related="category_id.approved_action_id"
    )
    is_manager_approver = fields.Boolean(
        related="category_id.is_manager_approver"
    )
    automated_sequence = fields.Boolean(
        related="category_id.automated_sequence"
    )
    resource_ref = fields.Reference(
        string="Ref",
        selection=lambda self: [
            (model.model, model.name)
            for model in self.env["ir.model"].search([])
        ],
        readonly=True,
        help="Optional field for reference to document created by action",
    )

    def _compute_has_access_to_request(self):
        is_request_user = self.env.user.has_group(
            "requests.group_request_user"
        )
        for request in self:
            request.has_access_to_request = (
                request.requested_by == self.env.user and is_request_user
            )

    def _compute_attachment_number(self):
        domain = [
            ("res_model", "=", "request.request"),
            ("res_id", "in", self.ids),
        ]
        attachment_data = self.env["ir.attachment"].read_group(
            domain, ["res_id"], ["res_id"]
        )
        attachment = {
            data["res_id"]: data["res_id_count"] for data in attachment_data
        }
        for request in self:
            request.attachment_number = attachment.get(request.id, 0)

    def _get_child_amount(self):
        """ Hook """
        self.ensure_one()
        return 0.0

    def _compute_child_amount(self):
        for rec in self:
            rec.child_amount = rec._get_child_amount()

    @api.onchange("category_id")
    def _onchange_category_id_set_defaults(self):
        if self.category_id.automated_sequence:
            self.name = self.category_id.sequence_id.next_by_id()
        else:
            self.name = self.category_id.name

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env["ir.actions.act_window"]._for_xml_id(
            "base.action_attachment"
        )
        res["domain"] = [
            ("res_model", "=", "request.request"),
            ("res_id", "in", self.ids),
        ]
        res["context"] = {
            "default_res_model": "request.request",
            "default_res_id": self.id,
        }
        return res

    def action_confirm(self):
        self.ensure_one()
        if self.use_approver and not self.approver_id:
            raise UserError(
                _("You have to select approver to confirm your request")
            )
        if self.has_document == "required" and not self.attachment_number:
            raise UserError(_("You have to attach at least one document."))
        self.write(
            {"date_confirmed": fields.Datetime.now(), "state": "pending"}
        )
        # Server Action
        for rec in self:
            rec.category_id.pending_action_id.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()

    def action_approve(self, approver=None):
        if self.approver_id and self.approver_id != self.env.user:
            raise UserError(_("You are not the approver of this request"))
        self.write({"state": "approved"})
        # Server Action
        for rec in self:
            rec.category_id.approved_action_id.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()

    def action_refuse(self, approver=None):
        self.write({"state": "refused"})
        # Server Action
        for rec in self:
            rec.category_id.refused_action_id.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()

    def action_withdraw(self, approver=None):
        self.write({"state": "pending"})

    def action_draft(self):
        self.write({"state": "draft"})
        # Server Action
        for rec in self:
            rec.category_id.draft_action_id.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()

    def action_cancel(self):
        self.write({"state": "cancel"})
        # Server Action
        for rec in self:
            rec.category_id.cancel_action_id.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()

    @api.onchange("category_id", "requested_by")
    def _onchange_category_id(self):
        if self.category_id.is_manager_approver:
            employee = self.env["hr.employee"].search(
                [("user_id", "=", self.requested_by.id)], limit=1
            )
            self.approver_id = employee.parent_id.user_id

    def execute_server_action(self):
        for rec in self:
            rec.category_id.approved_action_id.with_context(
                active_model=rec._name,
                active_id=rec.id,
            ).sudo().run()
