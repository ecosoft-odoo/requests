# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Requests -> Employee Advance Details",
    "version": "14.0.1.0.0",
    "category": "Human Resources/Requests",
    "website": "https://github.com/OCA/requests",
    "summary": """
        On employee advance request, allow adding advance details info.
    """,
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["requests_hr_advance", "hr_expense_advance_clearing_detail"],
    "application": False,
    "installable": True,
    "auto_install": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
