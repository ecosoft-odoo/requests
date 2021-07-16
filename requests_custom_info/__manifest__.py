# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Requests Custom Info",
    "summary": "Add custom info in requests",
    "author": "Ecosoft,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/requests",
    "category": "Usability",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base_custom_info", "requests"],
    "data": [
        "views/request_views.xml",
        "views/request_category_views.xml",
    ],
    "application": False,
    "development_status": "Beta",
    "maintainers": ["kittiu"],
}
