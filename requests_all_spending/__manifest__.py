# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Requests -> All Spending (PR/EX/AV)",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/account-payment",
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
