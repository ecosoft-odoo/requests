# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, SavepointCase


class TestRequestsHRExpense(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env.ref(
            "requests_hr_expense.request_category_data_hr_expense"
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

    def test_01_hr_expense(self):
        # Create new expense request and create expense.
        request_form = self.create_request_form(self.approver, self.category)
        with request_form.product_line_ids.new() as line:
            line.product_id = self.product_mouse
            line.quantity = 1
            line.price_unit = 100
        with request_form.product_line_ids.new() as line:
            line.product_id = self.product_mouse
            line.quantity = 2
            line.price_unit = 1000
        request = request_form.save()
        request.action_confirm()
        request.with_user(self.approver).action_approve()
        # Now, a EX should have been created
        self.assertEqual(request.hr_expense_count, 1)
        res = request.action_open_hr_expense()
        ex_id = res["domain"][0][2]
        expense = self.env["hr.expense.sheet"].browse(ex_id)
        self.assertEqual(len(expense.expense_line_ids), 2)
