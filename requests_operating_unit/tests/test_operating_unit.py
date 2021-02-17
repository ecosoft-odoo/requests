# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common


class TestOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestOperatingUnit, self).setUp()
        self.res_users_model = self.env["res.users"].with_context(
            tracking_disable=True, no_reset_password=True
        )

        # Groups
        self.grp_ou_mngr = self.env.ref(
            "operating_unit.group_manager_operating_unit"
        )
        self.grp_ou_multi = self.env.ref(
            "operating_unit.group_multi_operating_unit"
        )
        # Company
        self.company = self.env.ref("base.main_company")
        # Main operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2C operating Unit
        self.b2c = self.env.ref("operating_unit.b2c_operating_unit")
        # B2B operating Unit
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")
        # Create User 1 with Main ou
        self.user1 = self._create_user(
            "user_1", self.grp_ou_mngr, self.company, self.ou1
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2", self.grp_ou_multi, self.company, self.b2c
        )

    def _create_user(
        self, login, group, company, operating_units, context=None
    ):
        """ Create a user. """
        user = self.res_users_model.create(
            {
                "name": "Test User",
                "login": login,
                "password": "demo",
                "email": "test@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "default_operating_unit_id": operating_units[0].id,
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "sel_groups_13_14": group.id,
            }
        )
        return user

    def _create_request(self, user, name):
        """ Create Request"""
        category_test = self.env["request.category"].browse(1)

        record = (
            self.env["request.request"]
            .with_user(user.id)
            .create(
                {
                    "name": name,
                    "category_id": category_test.id,
                    "date_start": fields.Datetime.now(),
                    "date_end": fields.Datetime.now(),
                    "location": "testland",
                }
            )
        )
        return record

    def test_01_operating_unit(self):
        # User 1 tries to create and modify an ou
        # Create

        request1 = self._create_request(self.user1, "Test")
        self.assertEqual(
            request1.operating_unit_id.id,
            self.user1.default_operating_unit_id.id,
        )

        # Check search by user1
        request_list1 = (
            self.env["request.request"].with_user(self.user1.id).search([])
        )

        # User1 should see 3 request(2 Demo data(Main Operating Unit) + 1 New request)
        self.assertEqual(len(request_list1), 3)

        request_list2 = (
            self.env["request.request"].with_user(self.user2.id).search([])
        )

        self.assertEqual(len(request_list2), 0)
