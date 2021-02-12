# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        categ = env.ref(
            "requests_hr_advance.request_category_data_hr_advance", False
        )
        if categ:
            categ.write({"has_product": "no", "has_quantity": "no"})


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        categ = env.ref(
            "requests_hr_advance.request_category_data_hr_advance", False
        )
        if categ:
            categ.write(
                {"has_product": "optional", "has_quantity": "optional"}
            )
