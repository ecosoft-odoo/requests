# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RequestRequest(models.Model):
    _name = "request.request"
    _description = "Request Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    _check_company_auto = True

    @api.model
    def _read_group_request_status(self, stages, domain, order):
        request_status_list = dict(
            self._fields["request_status"].selection
        ).keys()
        return request_status_list

    name = fields.Char(string="Request Subject", tracking=True)
    category_id = fields.Many2one(
        "request.category", string="Category", required=True
    )
    approver_ids = fields.One2many(
        "request.approver",
        "request_id",
        string="Approvers",
        check_company=True,
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
    reason = fields.Text(string="Description")
    request_status = fields.Selection(
        [
            ("new", "To Submit"),
            ("pending", "Submitted"),
            ("approved", "Approved"),
            ("refused", "Refused"),
            ("cancel", "Cancel"),
        ],
        default="new",
        compute="_compute_request_status",
        store=True,
        tracking=True,
        group_expand="_read_group_request_status",
    )
    request_owner_id = fields.Many2one(
        "res.users",
        string="Request Owner",
        check_company=True,
        domain="[('company_ids', 'in', company_id)]",
    )
    user_status = fields.Selection(
        [
            ("new", "New"),
            ("pending", "To Approve"),
            ("approved", "Approved"),
            ("refused", "Refused"),
            ("cancel", "Cancel"),
        ],
        compute="_compute_user_status",
    )
    has_access_to_request = fields.Boolean(
        string="Has Access To Request",
        compute="_compute_has_access_to_request",
    )
    attachment_number = fields.Integer(
        "Number of Attachments", compute="_compute_attachment_number"
    )
    product_line_ids = fields.One2many(
        "request.product.line", "request_request_id", check_company=True
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
    requirer_document = fields.Selection(
        related="category_id.requirer_document"
    )
    request_minimum = fields.Integer(related="category_id.request_minimum")
    request_type = fields.Selection(related="category_id.request_type")
    is_manager_approver = fields.Boolean(
        related="category_id.is_manager_approver"
    )
    automated_sequence = fields.Boolean(
        related="category_id.automated_sequence"
    )

    def _compute_has_access_to_request(self):
        is_request_user = self.env.user.has_group(
            "requests.group_request_user"
        )
        for request in self:
            request.has_access_to_request = (
                request.request_owner_id == self.env.user and is_request_user
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
        if len(self.approver_ids) < self.request_minimum:
            raise UserError(
                _(
                    "You have to add at least %s approvers to confirm your request.",
                    self.request_minimum,
                )
            )
        if self.requirer_document == "required" and not self.attachment_number:
            raise UserError(_("You have to attach at lease one document."))
        approvers = self.mapped("approver_ids").filtered(
            lambda approver: approver.status == "new"
        )
        approvers._create_activity()
        approvers.write({"status": "pending"})
        self.write({"date_confirmed": fields.Datetime.now()})

    def _get_user_request_activities(self, user):
        domain = [
            ("res_model", "=", "request.request"),
            ("res_id", "in", self.ids),
            (
                "activity_type_id",
                "=",
                self.env.ref("requests.mail_activity_data_request").id,
            ),
            ("user_id", "=", user.id),
        ]
        activities = self.env["mail.activity"].search(domain)
        return activities

    def action_approve(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped("approver_ids").filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({"status": "approved"})
        self.sudo()._get_user_request_activities(
            user=self.env.user
        ).action_feedback()

    def action_refuse(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped("approver_ids").filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({"status": "refused"})
        self.sudo()._get_user_request_activities(
            user=self.env.user
        ).action_feedback()

    def action_withdraw(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped("approver_ids").filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({"status": "pending"})

    def action_draft(self):
        self.mapped("approver_ids").write({"status": "new"})

    def action_cancel(self):
        self.sudo()._get_user_request_activities(user=self.env.user).unlink()
        self.mapped("approver_ids").write({"status": "cancel"})

    @api.depends("approver_ids.status")
    def _compute_user_status(self):
        for request in self:
            request.user_status = request.approver_ids.filtered(
                lambda approver: approver.user_id == self.env.user
            ).status

    @api.depends("approver_ids.status")
    def _compute_request_status(self):
        for request in self:
            status_lst = request.mapped("approver_ids.status")
            minimal_approver = (
                request.request_minimum
                if len(status_lst) >= request.request_minimum
                else len(status_lst)
            )
            if status_lst:
                if status_lst.count("cancel"):
                    status = "cancel"
                elif status_lst.count("refused"):
                    status = "refused"
                elif status_lst.count("new"):
                    status = "new"
                elif status_lst.count("approved") >= minimal_approver:
                    status = "approved"
                else:
                    status = "pending"
            else:
                status = "new"
            request.request_status = status

    @api.onchange("category_id", "request_owner_id")
    def _onchange_category_id(self):
        current_users = self.approver_ids.mapped("user_id")
        new_users = self.category_id.user_ids
        if self.category_id.is_manager_approver:
            employee = self.env["hr.employee"].search(
                [("user_id", "=", self.request_owner_id.id)], limit=1
            )
            if employee.parent_id.user_id:
                new_users |= employee.parent_id.user_id
        for user in new_users - current_users:
            self.approver_ids += self.env["request.approver"].new(
                {"user_id": user.id, "request_id": self.id, "status": "new"}
            )


class RequestApprover(models.Model):
    _name = "request.approver"
    _description = "Approver"

    _check_company_auto = True

    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        check_company=True,
        domain="[('id', 'not in', existing_request_user_ids)]",
    )
    existing_request_user_ids = fields.Many2many(
        "res.users", compute="_compute_existing_request_user_ids"
    )
    status = fields.Selection(
        [
            ("new", "New"),
            ("pending", "To Approve"),
            ("approved", "Approved"),
            ("refused", "Refused"),
            ("cancel", "Cancel"),
        ],
        string="Status",
        default="new",
        readonly=True,
    )
    request_id = fields.Many2one(
        "request.request",
        string="Request",
        ondelete="cascade",
        check_company=True,
    )
    company_id = fields.Many2one(
        string="Company",
        related="request_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    def action_approve(self):
        self.request_id.action_approve(self)

    def action_refuse(self):
        self.request_id.action_refuse(self)

    def _create_activity(self):
        for approver in self:
            approver.request_id.activity_schedule(
                "requests.mail_activity_data_request",
                user_id=approver.user_id.id,
            )

    @api.depends(
        "request_id.request_owner_id", "request_id.approver_ids.user_id"
    )
    def _compute_existing_request_user_ids(self):
        for approver in self:
            approver.existing_request_user_ids = (
                self.mapped("request_id.approver_ids.user_id")._origin
                | self.request_id.request_owner_id._origin
            )
