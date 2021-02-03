# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests -> Employee Advance",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/account-payment",
    "summary": """
        This module adds to the requests workflow the possibility to generate
        Employee Advance from an Requests.
    """,
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["requests", "hr_expense_advance_clearing"],
    "data": [
        "data/ir_actions_server.xml",
        "data/request_category_data.xml",
        "views/request_views.xml",
    ],
    "demo": [
        "data/request_demo.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
