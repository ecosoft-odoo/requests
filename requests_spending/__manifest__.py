# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests for Multi Spending (PR/AV/EX)",
    "version": "14.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/requests",
    "summary": """
        This module adds to the requests workflow the possibility to generate
        mutiple spedings (PR/AV/EX) at the same time.
    """,
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "requests_purchase_request",
        "requests_hr_expense",
        "requests_hr_advance",
    ],
    "data": [
        "data/server_actions.xml",
        "data/request_category_data.xml",
    ],
    "application": False,
    "installable": True,
}
