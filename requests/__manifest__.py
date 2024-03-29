# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "category": "Tools",
    "website": "https://github.com/OCA/requests",
    "license": "AGPL-3",
    "summary": "Create and validate requests",
    "depends": ["mail", "hr", "product"],
    "data": [
        "security/request_security.xml",
        "security/ir.model.access.csv",
        "data/request_category_data.xml",
        "views/request_category_views.xml",
        "views/request_product_line_views.xml",
        "views/request_views.xml",
        "views/res_users_views.xml",
    ],
    "demo": [
        # "data/request_demo.xml",
    ],
    "application": True,
    "installable": True,
}
