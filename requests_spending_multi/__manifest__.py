# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests -> All Spending (PR/EX/AV)",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/requests",
    "summary": """
        This module adds to the requests workflow the possibility to generate
        Purchase Request from an Requests of Purchase Request.
    """,
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "requests_purchase_request",
        "requests_hr_expense",
        "requests_hr_advance",
    ],
    "data": [
        "data/request_category_data.xml",
        "views/request_views.xml",
        "views/request_category_views.xml",
        "views/request_product_line_views.xml",
    ],
    "demo": [
        "data/request_demo.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": True,
}
