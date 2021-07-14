# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo


@tagged("-at_install", "post_install")
class TestUi(HttpCaseWithUserDemo):
    def test_ui(self):
        self.env.ref("requests.request_category_data_business_trip").write(
            {
                "user_ids": [(4, self.env.ref("base.user_admin").id)],
            }
        )
        self.start_tour("/web", "requests_tour", login="admin")
