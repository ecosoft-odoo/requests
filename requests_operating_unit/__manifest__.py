# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests Operating Unit",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/requests",
    "category": "Tools",
    "depends": ["requests", "operating_unit"],
    "data": [
        "security/request_security.xml",
        "views/request_view.xml",
    ],
    "installable": True,
}
