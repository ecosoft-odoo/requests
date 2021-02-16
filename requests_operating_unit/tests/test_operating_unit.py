# © 2017-TODAY ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests import common


class TestOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestOperatingUnit, self).setUp()
        self.res_users_model = self.env["res.users"].with_context(
            tracking_disable=True, no_reset_password=True
        )

        # Groups
        self.grp_ou_mngr = self.env.ref(
            "requests_operating_unit.group_manager_operating_unit"
        )
        self.grp_ou_multi = self.env.ref(
            "requests_operating_unit.group_multi_operating_unit"
        )
        # Company
        self.company = self.env.ref("base.main_company")
        # Main operating Unit
        self.ou1 = self.env.ref("requests_operating_unit.main_operating_unit")
        # B2C operating Unit
        self.b2c = self.env.ref("requests_operating_unit.b2c_operating_unit")
        # B2B operating Unit
        self.b2b = self.env.ref("requests_operating_unit.b2b_operating_unit")
        # Create User 1 with Main ou
        self.user1 = self._create_user(
            "user_1", self.grp_ou_mngr, self.company, self.ou1
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2", self.grp_ou_multi, self.company, self.b2c
        )
        # Create User 3 with all OU
        self.user3 = self._create_user(
            "user_3",
            self.grp_ou_multi,
            self.company,
            [self.ou1, self.b2c, self.b2b],
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

    def _create_operating_unit(self, uid, name, code):
        """ Create operating Unit"""
        ou = (
            self.env["operating.unit"]
            .with_user(uid)
            .create(
                {"name": name, "code": code, "partner_id": self.company.id}
            )
        )
        return ou

    def _create_request(self, user, name):
        """ Create Request"""
        category_test = self.env["request.category"].browse(1)
        record = (
            self.env["request.request"]
            .with_user(user.id)
            .create(
                {
                    "name": name,
                    "operating_unit_id": user.default_operating_unit_id.id,
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
        self._create_operating_unit(self.user1.id, "Test", "TEST")
        # Write
        self.b2b.with_user(self.user1.id).write({"code": "B2B_changed"})
        # Read list of ou available by User 1
        operating_unit_list_1 = (
            self.env["operating.unit"]
            .with_user(self.user1.id)
            .search([])
            .mapped("code")
        )

        nou = self.env["operating.unit"].search(
            [
                "|",
                ("company_id", "=", False),
                ("company_id", "in", self.user1.company_ids.ids),
            ]
        )
        self.assertEqual(
            len(operating_unit_list_1),
            len(nou),
            "User 1 should have access to all the ou",
        )

        # User 2 tries to create and modify an OU
        with self.assertRaises(AccessError):
            # Create
            self._create_operating_unit(self.user2.id, "Test", "TEST")
        with self.assertRaises(AccessError):
            # Write
            self.b2b.with_user(self.user2.id).write({"code": "B2B_changed"})

        # Read list of OU available by User 2
        operating_unit_list_2 = (
            self.env["operating.unit"]
            .with_user(self.user2.id)
            .search([])
            .mapped("code")
        )
        self.assertEqual(
            len(operating_unit_list_2),
            1,
            "User 2 should have access to one ou",
        )
        self.assertEqual(
            operating_unit_list_2[0],
            "B2C",
            "User 2 should have access to " "%s" % self.b2c.name,
        )

        request1 = self._create_request(self.user1, "Test")
        self.assertEqual(
            request1.operating_unit_id.id,
            self.user1.default_operating_unit_id.id,
        )

        request2 = self._create_request(self.user2, "Test2")
        self.assertEqual(
            request2.operating_unit_id.id,
            self.user2.default_operating_unit_id.id,
        )

        # Check search by user1
        request_list1 = (
            self.env["request.request"].with_user(self.user1.id).search([])
        )

        # User1 should see 3 request(2 Demo data(No Operating Unit) + 1 New request)
        self.assertEqual(len(request_list1), 3)

        ou_list1 = self.env["operating.unit"].name_search(
            "B2B_changed", operator="ilike"
        )
        self.assertTrue(
            self.b2b
            in self.env["operating.unit"].browse(i[0] for i in ou_list1)
        )
