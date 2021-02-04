# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, SavepointCase


class TestRequestsHRAdvance(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env.ref(
            "requests_hr_advance.request_category_data_hr_advance"
        )
        cls.approver = cls.env.ref("base.user_admin")
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

    def test_01_hr_advance(self):
        # Create new advance request and create advance.
        request_form = self.create_request_form(self.approver, self.category)
        request_form.amount = 1000
        request = request_form.save()
        request.action_confirm()
        request.with_user(self.approver).action_approve()
        # Now, a AV should have been created
        self.assertEqual(request.hr_advance_count, 1)
        res = request.action_open_hr_advance()
        ex_id = res["domain"][0][2]
        expense = self.env["hr.expense.sheet"].browse(ex_id)
        self.assertTrue(expense.advance)
