# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def update_data_hooks(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        env.ref("base.group_user").write(
            {
                "implied_ids": [
                    (
                        4,
                        env.ref(
                            "hr_expense_widget_o2m.group_hr_expense_widget_o2m"
                        ).id,
                    ),
                ]
            }
        )
