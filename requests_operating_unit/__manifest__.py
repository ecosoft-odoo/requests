# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests_Operating_Unit",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/requests",
    "license": "AGPL-3",
    "summary": "Create and validate requests",
    "depends": ["mail", "hr", "product", "requests"],
    "data": [
        "security/operating_unit_security.xml",
        "security/ir.model.access.csv",
        "views/operating_unit_view.xml",
        "views/res_users_view.xml",
        "views/request_views.xml",
        "data/operating_unit_data.xml",
    ],
    "demo": ["demo/operating_unit_demo.xml"],
    "application": True,
    "installable": True,
    "auto_install": False,
}
