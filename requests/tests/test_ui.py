# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

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
