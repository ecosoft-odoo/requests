# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests_Operating_Unit",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/requests",
    "license": "AGPL-3",
    "summary": "Manage requests record rules by operating unit",
    "depends": ["requests", "operating_unit"],
    "data": [
        "views/request_views.xml",
        "security/operating_unit_security.xml",
    ],
    "installable": True,
    "auto_install": False,
}
