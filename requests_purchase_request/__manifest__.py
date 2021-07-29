# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests for Purchase Request",
    "version": "14.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/requests",
    "summary": """
        This module adds to the requests workflow the possibility to generate
        Purchase Request from an Requests for Purchase Request.
    """,
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["requests", "purchase_request"],
    "data": [
        "data/server_actions.xml",
        "views/request_views.xml",
        "views/request_category_views.xml",
        "views/purchase_request_views.xml",
    ],
    "demo": [
        "demo/request_category_data.xml",
    ],
    "application": False,
    "installable": True,
}
