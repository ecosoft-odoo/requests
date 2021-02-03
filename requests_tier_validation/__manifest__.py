# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests Tier Validation",
    "summary": "Extends the functionality of Requests to "
    "support a tier validation process.",
    "version": "14.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://github.com/OCA/account-payment",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["requests", "base_tier_validation"],
    "data": [
        "views/request_views.xml",
    ],
    "application": False,
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
