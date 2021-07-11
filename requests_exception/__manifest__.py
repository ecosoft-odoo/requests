# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Requests Exception",
    "summary": "Custom exceptions on requests",
    "version": "14.0.1.0.0",
    "category": "Generic Modules/Purchase",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/requests",
    "depends": ["requests", "base_exception", "requests_tier_validation"],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "wizard/request_exception_confirm_view.xml",
        "views/request_view.xml",
    ],
    "installable": True,
}
