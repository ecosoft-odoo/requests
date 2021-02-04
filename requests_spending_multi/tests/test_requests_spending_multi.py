# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, SavepointCase


class TestRequestsSpendingMulti(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env.ref(
            "requests_spending_multi.request_category_data_spending_multi"
        )
        cls.approver = cls.env.ref("base.user_admin")
        cls.product_mouse = cls.env["product.product"].create(
            {
                "name": "Computer Mouse",
            }
        )
        cls.product_laptop = cls.env["product.product"].create(
            {
                "name": "Laptop",
            }
        )
        advance_account = cls.env["account.account"].create(
            {
                "code": "154000",
                "name": "Employee Advance",
                "user_type_id": cls.env.ref(
                    "account.data_account_type_current_assets"
                ).id,
                "reconcile": True,
            }
        )
        cls.emp_advance = cls.env.ref(
            "hr_expense_advance_clearing.product_emp_advance"
        )
        cls.emp_advance.property_account_expense_id = advance_account

    def create_request_form(self, approver, category):
        if category.automated_sequence:
            name = category.sequence_id.next_by_id()
        else:
            name = category.name
        create_request_form = Form(
            self.env["request.request"].with_context(
                default_name=name,
                default_category_id=category.id,
                default_request_owner_id=approver.id,
            )
        )
        with create_request_form.approver_ids.new() as req_approver:
            req_approver.user_id = approver
        return create_request_form

    def test_01_spending_multi(self):
        # Create new spending request request and create PR/AV/EX.
        request_form = self.create_request_form(self.approver, self.category)
        request_form.amount = 1000  # AV
        with request_form.product_line_ids.new() as line:
            line.product_id = self.product_mouse
            line.quantity = 1
            line.price_unit = 100
            line.res_type = "ex"  # EX
        with request_form.product_line_ids.new() as line:
            line.product_id = self.product_mouse
            line.quantity = 2
            line.price_unit = 1000
            line.res_type = "pr"  # PR
        request = request_form.save()
        request.action_confirm()
        request.with_user(self.approver).action_approve()
        # Now, all PR/AV/EX should have been created
        # PR
        self.assertEqual(request.purchase_request_count, 1)
        res = request.action_open_purchase_request()
        pr_id = res["domain"][0][2]
        purchase_request = self.env["purchase.request"].browse(pr_id)
        self.assertEqual(len(purchase_request.line_ids), 1)
        # EX
        self.assertEqual(request.hr_expense_count, 1)
        res = request.action_open_hr_expense()
        ex_id = res["domain"][0][2]
        expense = self.env["hr.expense.sheet"].browse(ex_id)
        self.assertEqual(len(expense.expense_line_ids), 1)
        # AV
        self.assertEqual(request.hr_advance_count, 1)
        self.assertEqual(request.hr_advance_count, 1)
        res = request.action_open_hr_advance()
        av_id = res["domain"][0][2]
        advance = self.env["hr.expense.sheet"].browse(av_id)
        self.assertTrue(advance.advance)
