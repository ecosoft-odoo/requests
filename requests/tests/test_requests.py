# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import common


class TestRequest(common.TransactionCase):
    def test_01_compute_state(self):
        category_test = self.env["request.category"].browse(1)
        record = self.env["request.request"].create(
            {
                "name": "test request",
                "category_id": category_test.id,
                "date_start": fields.Datetime.now(),
                "date_end": fields.Datetime.now(),
                "location": "testland",
            }
        )
        first_approver = self.env["request.approver"].create(
            {"user_id": 1, "request_id": record.id, "status": "new"}
        )
        second_approver = self.env["request.approver"].create(
            {"user_id": 2, "request_id": record.id, "status": "new"}
        )
        record.approver_ids += first_approver
        record.approver_ids += second_approver

        self.assertEqual(record.state, "new")

        record.action_confirm()

        # Test case 1: Min request = 1
        self.assertEqual(record.state, "pending")
        record.action_approve(first_approver)
        self.assertEqual(record.state, "approved")
        record.action_approve(second_approver)
        self.assertEqual(record.state, "approved")
        record.action_withdraw(first_approver)
        self.assertEqual(record.state, "approved")
        record.action_refuse(first_approver)
        self.assertEqual(record.state, "refused")

        # Test case 2: Min request = 1
        category_test.request_minimum = 2
        record.action_withdraw(first_approver)
        record.action_withdraw(second_approver)
        self.assertEqual(record.state, "pending")
        record.action_approve(first_approver)
        self.assertEqual(record.state, "pending")
        record.action_approve(second_approver)
        self.assertEqual(record.state, "approved")
        record.action_withdraw(second_approver)
        self.assertEqual(record.state, "pending")
        record.action_refuse(second_approver)
        self.assertEqual(record.state, "refused")

        # Test case 3: Check that cancel is erasing the old validations
        record.action_cancel()
        self.assertEqual(first_approver.status, "cancel")
        self.assertEqual(second_approver.status, "cancel")
        self.assertEqual(record.state, "cancel")

        # Test case 4: Set the request request to draft
        record.action_draft()
        self.assertEqual(first_approver.status, "new")
        self.assertEqual(second_approver.status, "new")
        self.assertEqual(record.state, "new")

        # Test case 5: Set min request to an impossible value to reach
        category_test.request_minimum = 3
        with self.assertRaises(UserError):
            record.action_confirm()
        self.assertEqual(record.state, "new")

    def test_02_context_overwrite(self):
        category_test = self.env["request.category"].browse(1)
        category_test.context_overwrite = (
            "{'default_amount': 100, 'xxx': env.user.id}"
        )
        res = category_test.create_request()
        context = res.get("context", {})
        self.assertEqual(context.get("default_amount"), 100)
